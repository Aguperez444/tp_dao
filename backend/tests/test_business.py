import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from app.application.dto.commands.line_command import LineCommand
from app.application.dto.commands.order_command import OrderCommand
from app.application.dto.commands.product_command import ProductCommand
from app.application.dto.commands.supplier_command import SupplierCommand
from app.application.dto.commands.transition_command import TransitionCommand
from app.domain.exceptions.business_error import BusinessError
from app.domain.services.money_service import to_cents
from app.infrastructure.database.database import Database
from app.seed import seed
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from tests.helpers import Fixture


class BusinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Database(Path(self.tmp.name) / "test.sqlite3")
        self.db.initialize()
        self.addCleanup(self.db.dispose)
        self.f = Fixture(self.db)

    def test_schema_matches_der(self):
        tables = set(inspect(self.db.engine).get_table_names())
        self.assertEqual(len(tables), 27)
        self.assertIn("cambio_estado_bulto", tables)
        self.assertNotIn("pagos", tables)
        self.assertNotIn("solicitudes", tables)
        columns = {
            x["name"] for x in inspect(self.db.engine).get_columns("detalle_venta")
        }
        self.assertIn("costo_unitario", columns)

    def test_purchase_requires_receipt_once(self):
        p = self.f.purchase(receive=False)
        self.assertEqual(self.f.stock(self.f.cd), (0, 0))
        self.f.receive_purchase.execute(p.id)
        self.assertEqual(self.f.stock(self.f.cd), (100, 0))
        with self.assertRaises(BusinessError):
            self.f.receive_purchase.execute(p.id)
        self.assertEqual(self.f.stock(self.f.cd), (100, 0))

    def test_all_packages_and_delivery_must_be_verified(self):
        self.f.purchase()
        o = self.f.order()
        r = self.f.delivery(o)
        a = self.f.package(r, 5)
        b = self.f.package(r, 5)
        self.assertEqual(self.f.stock(self.f.cd), (100, 10))
        self.f.seal(a)
        self.f.seal(b)
        self.f.receive(a)
        self.f.receive(b)
        self.assertEqual(self.f.stock(self.f.local), (0, 0))
        self.f.verify(a, r)
        self.assertEqual(self.f.stock(self.f.local), (0, 0))
        self.f.verify(b, r)
        self.assertEqual(self.f.stock(self.f.local), (10, 0))
        self.assertEqual(self.f.stock(self.f.cd), (90, 0))
        self.assertEqual(self.f.query_orders.execute()[0].estado, "Completada")
        with self.assertRaises(BusinessError):
            self.f.verify(b, r)
        self.assertEqual(self.f.stock(self.f.local), (10, 0))

    def test_one_rejection_blocks_whole_delivery(self):
        self.f.purchase()
        o = self.f.order()
        r = self.f.delivery(o)
        a = self.f.package(r, 5)
        b = self.f.package(r, 5)
        self.f.seal(a)
        self.f.seal(b)
        self.f.receive(a)
        self.f.receive(b)
        self.f.verify(a, r, precinto_intacto=False, observacion="Precinto roto")
        self.f.verify(b, r)
        self.assertEqual(self.f.stock(self.f.local), (0, 0))
        self.assertEqual(
            self.f.query_orders.execute()[0].remitos[0].estado, "Rechazado"
        )
        with self.assertRaises(BusinessError):
            self.f.sell()

    def test_mismatched_seal_or_delivery_rejects(self):
        for field in ("codigo_precinto", "numero_remito"):
            with self.subTest(field=field):
                self.f.purchase()
                o = self.f.order(1)
                r = self.f.delivery(o)
                b = self.f.package(r, 1)
                self.f.seal(b)
                self.f.receive(b)
                result = self.f.verify(
                    b, r, **{field: "INCORRECTO", "observacion": "Número no coincide"}
                )
                self.assertEqual(result.estado, "Rechazado")
        self.assertEqual(self.f.stock(self.f.local), (0, 0))

    def test_rejection_requires_reason_and_preserves_state_on_error(self):
        self.f.purchase()
        o = self.f.order()
        r = self.f.delivery(o)
        b = self.f.package(r)
        self.f.seal(b)
        self.f.receive(b)
        with self.assertRaises(BusinessError):
            self.f.verify(b, r, precinto_intacto=False)
        with self.db.uow() as u:
            self.assertEqual(len(u.cambio_estado_bulto_repo.list(bulto_id=b.id)), 4)

    def test_state_no_skips_and_no_direct_verify(self):
        self.f.purchase()
        o = self.f.order()
        r = self.f.delivery(o)
        b = self.f.package(r)
        for action in ("recibir", "verificar", "rechazar", "despachar"):
            with self.assertRaises(BusinessError):
                self.f.transition_package.execute(
                    b.id, action, TransitionCommand(responsable="Ana")
                )

    def test_history_is_append_only(self):
        self.f.supply()
        for statement in (
            'UPDATE cambio_estado_bulto SET responsable="Otro"',
            "DELETE FROM cambio_estado_bulto",
        ):
            with self.assertRaises(IntegrityError):
                with self.db.engine.begin() as cx:
                    cx.execute(text(statement))

    def test_reservation_rollback_when_another_line_has_no_stock(self):
        self.f.purchase()
        o = self.f.order(10, 30)
        r = self.f.delivery(o)
        with self.assertRaises(BusinessError):
            self.f.package(r, 10, 30)
        self.assertEqual(self.f.stock(self.f.cd), (100, 0))
        with self.db.uow() as u:
            self.assertEqual(u.bulto_repo.list(), [])
            self.assertEqual(u.cambio_estado_bulto_repo.list(), [])

    def test_cannot_overpack_order_or_add_after_dispatch(self):
        self.f.purchase()
        o = self.f.order(10)
        r = self.f.delivery(o)
        with self.assertRaises(BusinessError):
            self.f.package(r, 11)
        a = self.f.package(r, 5)
        self.f.seal(a)
        self.f.receive(a)
        with self.assertRaises(BusinessError):
            self.f.package(r, 5)

    def test_all_packages_must_be_sealed_before_dispatch(self):
        self.f.purchase()
        o = self.f.order()
        r = self.f.delivery(o)
        a = self.f.package(r, 5)
        self.f.package(r, 5)
        self.f.seal(a)
        with self.assertRaises(BusinessError):
            self.f.receive(a)
        self.assertEqual(self.f.stock(self.f.cd), (100, 10))

    def test_multiple_deliveries_can_fulfil_one_order(self):
        self.f.purchase()
        o = self.f.order(10)
        for _ in range(2):
            r = self.f.delivery(o)
            b = self.f.package(r, 5)
            self.f.seal(b)
            self.f.receive(b)
            self.f.verify(b, r)
        self.assertEqual(self.f.stock(self.f.local), (10, 0))
        self.assertEqual(self.f.query_orders.execute()[0].estado, "Completada")

    def test_duplicate_seal_rolls_back(self):
        self.f.purchase()
        o = self.f.order()
        r = self.f.delivery(o)
        a = self.f.package(r, 5)
        b = self.f.package(r, 5)
        self.f.seal(a)
        with self.assertRaises(IntegrityError):
            self.f.transition_package.execute(
                b.id,
                "precintar",
                TransitionCommand(responsable="Ana", codigo_precinto=f"S-{a.id}"),
            )
        with self.db.uow() as u:
            self.assertEqual(len(u.cambio_estado_bulto_repo.list(bulto_id=b.id)), 1)

    def test_only_cd_to_local_and_sales_in_local(self):
        with self.assertRaises(BusinessError):
            self.f.create_order.execute(
                OrderCommand(
                    establecimiento_solicitante_id=self.f.cd,
                    establecimiento_proveedor_id=self.f.local,
                    detalles=[LineCommand(producto_id=self.f.p, cantidad=1)],
                )
            )
        self.f.purchase()
        with self.assertRaises(BusinessError):
            self.f.sell(local_id=self.f.cd)

    def test_wrong_payment_rolls_back_sale(self):
        self.f.supply()
        with self.assertRaises(BusinessError):
            self.f.sell(importe_cobrado="1")
        self.assertEqual(self.f.stock(self.f.local), (10, 0))
        self.assertEqual(self.f.query_sales.execute(), [])

    def test_two_concurrent_sales_cannot_sell_last_unit_twice(self):
        self.f.supply(1)

        def sell(_):
            try:
                self.f.sell()
                return True
            except BusinessError:
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(pool.map(sell, [1, 2])), 1)
        self.assertEqual(self.f.stock(self.f.local), (0, 0))

    def test_two_concurrent_verifications_do_not_double_credit(self):
        self.f.purchase()
        o = self.f.order(1)
        r = self.f.delivery(o)
        b = self.f.package(r, 1)
        self.f.seal(b)
        self.f.receive(b)

        def verify(_):
            try:
                self.f.verify(b, r)
                return True
            except BusinessError:
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(pool.map(verify, [1, 2])), 1)
        self.assertEqual(self.f.stock(self.f.local), (1, 0))

    def test_refunds_use_original_prices_and_costs(self):
        self.f.supply()
        sale = self.f.sell(2)
        self.f.save_catalog(
            "producto",
            ProductCommand(
                codigo="A",
                nombre="Arroz",
                detalle="",
                categoria_id=self.f.category,
                precio="300",
                costo_referencia="250",
                esta_activo=True,
            ),
            self.f.p,
        )
        self.f.refund(sale)
        detail = self.f.get_sale.execute(sale.id)
        self.assertEqual(detail.devoluciones[0].total, 10000)
        self.assertEqual(detail.detalles[0].costo_unitario, 6000)
        report = self.f.reports.generate("2000", "9999")
        self.assertEqual(report.productos[0].margen_estimado, 4000)
        self.assertEqual(self.f.stock(self.f.local), (9, 0))

    def test_refund_quantity_accumulates(self):
        self.f.supply()
        sale = self.f.sell(3)
        self.f.refund(sale, 2)
        with self.assertRaises(BusinessError):
            self.f.refund(sale, 2)
        self.f.refund(sale, 1)
        self.assertEqual(self.f.stock(self.f.local), (10, 0))
        self.assertEqual(
            sum((x.neto for x in self.f.reports.generate("2000", "9999").ventas)), 0
        )

    def test_two_concurrent_refunds_do_not_exceed_sale(self):
        self.f.supply()
        sale = self.f.sell()

        def refund(_):
            try:
                self.f.refund(sale)
                return True
            except BusinessError:
                return False

        with ThreadPoolExecutor(max_workers=2) as pool:
            self.assertEqual(sum(pool.map(refund, [1, 2])), 1)
        self.assertEqual(self.f.stock(self.f.local), (10, 0))

    def test_refund_must_be_original_product_and_apt(self):
        self.f.supply()
        sale = self.f.sell()
        with self.assertRaises(BusinessError):
            self.f.refund(
                sale, detalles=[LineCommand(producto_id=self.f.p2, cantidad=1)]
            )
        with self.assertRaises(BusinessError):
            self.f.refund(sale, productos_aptos=False)
        self.assertEqual(self.f.stock(self.f.local), (9, 0))

    def test_refund_has_time_limit(self):
        self.f.supply()
        sale = self.f.sell()
        with self.db.uow(write=True) as u:
            entity = u.venta_repo.get(sale.id)
            entity.fecha = (datetime.now(timezone.utc) - timedelta(days=31)).isoformat()
            u.venta_repo.update(entity)
        with self.assertRaises(BusinessError):
            self.f.refund(sale)

    def test_discount_strategy_is_refunded_at_discounted_price(self):
        self.f.supply()
        sale = self.f.sell(politica="descuento_10", importe_cobrado="90")
        self.assertEqual(sale.detalles[0].descuento_aplicado, 1000)
        self.assertEqual(sale.total, 9000)
        self.f.refund(sale)
        self.assertEqual(self.f.get_sale.execute(sale.id).devoluciones[0].total, 9000)

    def test_inactive_product_cannot_sell_but_can_be_returned(self):
        self.f.supply()
        sale = self.f.sell()
        self.f.save_catalog(
            "producto",
            ProductCommand(
                codigo="A",
                nombre="Arroz",
                detalle="",
                categoria_id=self.f.category,
                precio="100",
                costo_referencia="60",
                esta_activo=False,
            ),
            self.f.p,
        )
        with self.assertRaises(BusinessError):
            self.f.sell()
        self.f.refund(sale)
        self.assertEqual(self.f.stock(self.f.local), (10, 0))

    def test_unique_normalized_identifiers(self):
        with self.assertRaises(IntegrityError):
            self.f.save_catalog(
                "proveedor",
                SupplierCommand(nombre="Otro", CUIT="30000000000", esta_activo=True),
            )
        with self.assertRaises(IntegrityError):
            self.f.save_catalog(
                "producto",
                ProductCommand(
                    codigo=" a ",
                    nombre="Otro",
                    detalle="",
                    categoria_id=self.f.category,
                    precio="1",
                    costo_referencia="1",
                    esta_activo=True,
                ),
            )

    def test_report_filters_and_movement_reconciliation(self):
        self.f.supply()
        sale = self.f.sell(2)
        self.f.refund(sale)
        self.assertEqual(
            sum((x.neto for x in self.f.reports.generate("2000", "9999").ventas)), 10000
        )
        self.assertEqual(self.f.reports.generate("2000", "2001").ventas, [])
        self.assertEqual(
            self.f.reports.generate("2000", "9999", self.f.north).productos, []
        )
        movements = self.f.reports.movements("2000", "9999")
        for stock in self.f.reports.stock():
            total = sum(
                (
                    m.cantidad
                    for m in movements
                    if m.establecimiento == stock.establecimiento
                    and m.codigo == stock.codigo
                )
            )
            self.assertEqual(total, stock.almacenado_total)

    def test_money_rejects_nonfinite_negative_or_excess_precision(self):
        self.assertEqual(to_cents("0.29"), 29)
        for value in ("NaN", "Infinity", "-1", "1.001"):
            with self.assertRaises(BusinessError):
                to_cents(value)

    def test_demo_cannot_overwrite_existing_business_data(self):
        with self.assertRaises(BusinessError):
            seed(self.db)
        self.assertEqual(len(self.f.query_catalogs.execute().establecimiento), 3)


if __name__ == "__main__":
    unittest.main()
