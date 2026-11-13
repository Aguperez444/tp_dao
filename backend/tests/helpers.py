from dataclasses import replace

from app.application.dto.commands.address_command import AddressCommand
from app.application.dto.commands.city_command import CityCommand
from app.application.dto.commands.establishment_command import EstablishmentCommand
from app.application.dto.commands.line_command import LineCommand
from app.application.dto.commands.named_command import NamedCommand
from app.application.dto.commands.order_command import OrderCommand
from app.application.dto.commands.package_command import PackageCommand
from app.application.dto.commands.product_command import ProductCommand
from app.application.dto.commands.purchase_command import PurchaseCommand
from app.application.dto.commands.purchase_line_command import PurchaseLineCommand
from app.application.dto.commands.refund_command import RefundCommand
from app.application.dto.commands.sale_command import SaleCommand
from app.application.dto.commands.supplier_command import SupplierCommand
from app.application.dto.commands.transition_command import TransitionCommand
from app.application.use_cases.create_delivery import CreateDelivery
from app.application.use_cases.create_purchase import CreatePurchase
from app.application.use_cases.create_replenishment_order import (
    CreateReplenishmentOrder,
)
from app.application.use_cases.create_sale import CreateSale
from app.application.use_cases.get_sale import GetSale
from app.application.use_cases.prepare_package import PreparePackage
from app.application.use_cases.query_catalogs import QueryCatalogs
from app.application.use_cases.query_purchases import QueryPurchases
from app.application.use_cases.query_replenishment_orders import (
    QueryReplenishmentOrders,
)
from app.application.use_cases.query_sales import QuerySales
from app.application.use_cases.quote_sale import QuoteSale
from app.application.use_cases.receive_purchase import ReceivePurchase
from app.application.use_cases.refund_sale import RefundSale
from app.application.use_cases.save_categoria import SaveCategoria
from app.application.use_cases.save_ciudad import SaveCiudad
from app.application.use_cases.save_domicilio import SaveDomicilio
from app.application.use_cases.save_establecimiento import SaveEstablecimiento
from app.application.use_cases.save_motivo import SaveMotivo
from app.application.use_cases.save_producto import SaveProducto
from app.application.use_cases.save_proveedor import SaveProveedor
from app.application.use_cases.save_provincia import SaveProvincia
from app.application.use_cases.set_stock_minimum import SetStockMinimum
from app.application.use_cases.transition_package import TransitionPackage
from app.infrastructure.database.repositories.reports_repository_impl import (
    ReportsRepositoryImpl,
)


class Fixture:
    def __init__(self, database):
        self.db = database
        self.query_catalogs = QueryCatalogs(database.uow)
        self.set_minimum = SetStockMinimum(database.uow)
        self.create_purchase = CreatePurchase(database.uow)
        self.receive_purchase = ReceivePurchase(database.uow)
        self.query_purchases = QueryPurchases(database.uow)
        self.create_order = CreateReplenishmentOrder(database.uow)
        self.create_delivery = CreateDelivery(database.uow)
        self.prepare_package = PreparePackage(database.uow)
        self.transition_package = TransitionPackage(database.uow)
        self.query_orders = QueryReplenishmentOrders(database.uow)
        self.quote_sale = QuoteSale(database.uow)
        self.create_sale = CreateSale(database.uow)
        self.refund_sale = RefundSale(database.uow)
        self.get_sale = GetSale(database.uow)
        self.query_sales = QuerySales(database.uow)
        self.reports = ReportsRepositoryImpl(database)
        province = self.save_catalog("provincia", NamedCommand(nombre="Córdoba")).id
        city = self.save_catalog(
            "ciudad", CityCommand(nombre="Córdoba", provincia_id=province)
        ).id
        address = self.save_catalog(
            "domicilio", AddressCommand(calle="Ejemplo", altura="123", ciudad_id=city)
        ).id
        self.cd = self.save_catalog(
            "establecimiento",
            EstablishmentCommand(nombre="CD", es_central=True, domicilio_id=address),
        ).id
        self.local = self.save_catalog(
            "establecimiento",
            EstablishmentCommand(
                nombre="Centro", es_central=False, domicilio_id=address
            ),
        ).id
        self.north = self.save_catalog(
            "establecimiento",
            EstablishmentCommand(
                nombre="Norte", es_central=False, domicilio_id=address
            ),
        ).id
        self.category = self.save_catalog(
            "categoria", NamedCommand(nombre="Almacén")
        ).id
        self.supplier = self.save_catalog(
            "proveedor",
            SupplierCommand(nombre="Proveedor", CUIT="30-00000000-0", esta_activo=True),
        ).id
        self.p = self.save_catalog(
            "producto",
            ProductCommand(
                codigo="A",
                nombre="Arroz",
                detalle="",
                categoria_id=self.category,
                precio="100",
                costo_referencia="60",
                esta_activo=True,
            ),
        ).id
        self.p2 = self.save_catalog(
            "producto",
            ProductCommand(
                codigo="B",
                nombre="Aceite",
                detalle="",
                categoria_id=self.category,
                precio="200",
                costo_referencia="120",
                esta_activo=True,
            ),
        ).id
        with database.uow() as u:
            self.method = u.metodo_pago_repo.list()[0].id
            self.reason = u.motivo_repo.list()[0].id
        self._counter = 0

    def purchase(self, receive=True):
        p = self.create_purchase.execute(
            PurchaseCommand(
                proveedor_id=self.supplier,
                detalles=[
                    PurchaseLineCommand(producto_id=self.p, cantidad=100, costo="60"),
                    PurchaseLineCommand(producto_id=self.p2, cantidad=20, costo="120"),
                ],
            )
        )
        if receive:
            self.receive_purchase.execute(p.id)
        return p

    def order(self, quantity=10, second=0):
        details = [LineCommand(producto_id=self.p, cantidad=quantity)]
        if second:
            details.append(LineCommand(producto_id=self.p2, cantidad=second))
        return self.create_order.execute(
            OrderCommand(
                establecimiento_solicitante_id=self.local,
                establecimiento_proveedor_id=self.cd,
                detalles=details,
            )
        )

    def delivery(self, order):
        self._counter += 1
        return self.create_delivery.execute(order.id, f"R-{self._counter}")

    def package(self, delivery, quantity=10, second=0):
        lines = [LineCommand(producto_id=self.p, cantidad=quantity)]
        if second:
            lines.append(LineCommand(producto_id=self.p2, cantidad=second))
        return self.prepare_package.execute(
            delivery.id, PackageCommand(responsable="Ana", detalles=lines)
        )

    def seal(self, package):
        return self.transition_package.execute(
            package.id,
            "precintar",
            TransitionCommand(responsable="Ana", codigo_precinto=f"S-{package.id}"),
        )

    def receive(self, package):
        self.transition_package.execute(
            package.id, "despachar", TransitionCommand(responsable="Ana")
        )
        self.transition_package.execute(
            package.id, "recibir", TransitionCommand(responsable="Luis")
        )

    def verify(self, package, delivery, **extra):
        data = TransitionCommand(
            responsable="Luis",
            codigo_precinto=f"S-{package.id}",
            numero_remito=delivery.numero_remito,
            precinto_intacto=True,
            contenido_conforme=True,
        )
        return self.transition_package.execute(
            package.id, "inspeccionar", replace(data, **extra)
        )

    def supply(self, quantity=10):
        self.purchase()
        order = self.order(quantity)
        delivery = self.delivery(order)
        package = self.package(delivery, quantity)
        self.seal(package)
        self.receive(package)
        self.verify(package, delivery)
        return (package, delivery)

    def stock(self, establishment, product=None):
        with self.db.uow() as u:
            rows = u.existencia_repo.list(
                establecimiento_id=establishment, producto_id=product or self.p
            )
            return (rows[0].almacenado_total, rows[0].reservado) if rows else (0, 0)

    def sell(self, quantity=1, **extra):
        data = SaleCommand(
            local_id=self.local,
            metodo_pago_id=self.method,
            politica="lista",
            importe_cobrado=str(quantity * 100),
            detalles=[LineCommand(producto_id=self.p, cantidad=quantity)],
        )
        return self.create_sale.execute(replace(data, **extra))

    def refund(self, sale, quantity=1, **extra):
        data = RefundCommand(
            motivo_id=self.reason,
            metodo_reintegro_id=self.method,
            detalle="Cambio solicitado",
            productos_aptos=True,
            detalles=[LineCommand(producto_id=self.p, cantidad=quantity)],
        )
        return self.refund_sale.execute(sale.id, replace(data, **extra))

    def save_catalog(self, table, data, id=None):
        use_cases = {
            "categoria": SaveCategoria,
            "provincia": SaveProvincia,
            "ciudad": SaveCiudad,
            "domicilio": SaveDomicilio,
            "establecimiento": SaveEstablecimiento,
            "proveedor": SaveProveedor,
            "producto": SaveProducto,
            "motivo": SaveMotivo,
        }
        return use_cases[table](self.db.uow).execute(data, id)
