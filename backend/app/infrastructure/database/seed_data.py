from __future__ import annotations

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
from app.application.use_cases.prepare_package import PreparePackage
from app.application.use_cases.receive_purchase import ReceivePurchase
from app.application.use_cases.refund_sale import RefundSale
from app.application.use_cases.save_categoria import SaveCategoria
from app.application.use_cases.save_ciudad import SaveCiudad
from app.application.use_cases.save_domicilio import SaveDomicilio
from app.application.use_cases.save_establecimiento import SaveEstablecimiento
from app.application.use_cases.save_producto import SaveProducto
from app.application.use_cases.save_proveedor import SaveProveedor
from app.application.use_cases.save_provincia import SaveProvincia
from app.application.use_cases.set_stock_minimum import SetStockMinimum
from app.application.use_cases.transition_package import TransitionPackage
from app.domain.exceptions.business_error import BusinessError
from app.infrastructure.database.database import Database
from app.infrastructure.database.unit_of_work.shared_unit_of_work import (
    SharedUnitOfWork,
)


def seed(database: Database) -> None:
    with database.uow(write=True) as u:
        if any(
            (
                u.establecimiento_repo.list(),
                u.producto_repo.list(),
                u.proveedor_repo.list(),
                u.provincia_repo.list(),
                u.categoria_repo.list(),
                u.compra_repo.list(),
                u.venta_repo.list(),
            )
        ):
            raise BusinessError(
                "La demo solo se puede cargar en una base vacía; sus datos actuales se conservan."
            )
    with database.uow(write=True) as root:

        def factory(*, write: bool = False) -> SharedUnitOfWork:
            return SharedUnitOfWork(root)

        if (
            root.establecimiento_repo.list()
            or root.producto_repo.list()
            or root.provincia_repo.list()
        ):
            raise BusinessError("La base ya contiene datos.")
        province = SaveProvincia(factory).execute(NamedCommand(nombre="Córdoba")).id
        city = (
            SaveCiudad(factory)
            .execute(CityCommand(nombre="Córdoba", provincia_id=province))
            .id
        )
        establishments = []
        for name, street, height, central in [
            ("Centro de distribución", "Av. Circunvalación", "1200", True),
            ("Local Centro", "San Martín", "245", False),
            ("Local Norte", "Av. Rafael Núñez", "4100", False),
        ]:
            address = (
                SaveDomicilio(factory)
                .execute(AddressCommand(calle=street, altura=height, ciudad_id=city))
                .id
            )
            establishments.append(
                SaveEstablecimiento(factory)
                .execute(
                    EstablishmentCommand(
                        nombre=name, es_central=central, domicilio_id=address
                    )
                )
                .id
            )
        cd, center, north = establishments
        category = SaveCategoria(factory).execute(NamedCommand(nombre="Almacén")).id
        supplier = (
            SaveProveedor(factory)
            .execute(
                SupplierCommand(
                    nombre="Distribuidora de ejemplo",
                    CUIT="30-00000000-0",
                    esta_activo=True,
                )
            )
            .id
        )
        products = []
        for code, name, price, cost in [
            ("YER-001", "Yerba mate 1 kg", "6500", "4000"),
            ("CAF-001", "Café molido 250 g", "4800", "2900"),
            ("AZU-001", "Azúcar 1 kg", "1800", "1000"),
        ]:
            products.append(
                SaveProducto(factory)
                .execute(
                    ProductCommand(
                        codigo=code,
                        nombre=name,
                        detalle="Producto de demostración",
                        categoria_id=category,
                        precio=price,
                        costo_referencia=cost,
                        esta_activo=True,
                    )
                )
                .id
            )
        purchase = CreatePurchase(factory).execute(
            PurchaseCommand(
                proveedor_id=supplier,
                detalles=[
                    PurchaseLineCommand(producto_id=p, cantidad=100, costo=c)
                    for p, c in zip(products, ["4000", "2900", "1000"])
                ],
            )
        )
        ReceivePurchase(factory).execute(purchase.id)
        for establishment in establishments:
            for product in products:
                SetStockMinimum(factory).execute(establishment, product, 10)
        order = CreateReplenishmentOrder(factory).execute(
            OrderCommand(
                establecimiento_solicitante_id=center,
                establecimiento_proveedor_id=cd,
                detalles=[
                    LineCommand(producto_id=p, cantidad=q)
                    for p, q in zip(products, [20, 15, 30])
                ],
            )
        )
        delivery = CreateDelivery(factory).execute(order.id, "R-DEMO-001")
        packages = []
        for lines in [
            [
                LineCommand(producto_id=products[0], cantidad=20),
                LineCommand(producto_id=products[1], cantidad=15),
            ],
            [LineCommand(producto_id=products[2], cantidad=30)],
        ]:
            packages.append(
                PreparePackage(factory).execute(
                    delivery.id, PackageCommand(responsable="Ana Demo", detalles=lines)
                )
            )
        for i, package in enumerate(packages, 1):
            TransitionPackage(factory).execute(
                package.id,
                "precintar",
                TransitionCommand(
                    responsable="Ana Demo", codigo_precinto=f"P-DEMO-{i}"
                ),
            )
        for i, package in enumerate(packages, 1):
            TransitionPackage(factory).execute(
                package.id, "despachar", TransitionCommand(responsable="Ana Demo")
            )
            TransitionPackage(factory).execute(
                package.id, "recibir", TransitionCommand(responsable="Luis Demo")
            )
            TransitionPackage(factory).execute(
                package.id,
                "inspeccionar",
                TransitionCommand(
                    responsable="Luis Demo",
                    codigo_precinto=f"P-DEMO-{i}",
                    numero_remito="R-DEMO-001",
                    precinto_intacto=True,
                    contenido_conforme=True,
                ),
            )
        sale = CreateSale(factory).execute(
            SaleCommand(
                local_id=center,
                metodo_pago_id=root.metodo_pago_repo.list()[0].id,
                politica="lista",
                importe_cobrado="29100",
                detalles=[
                    LineCommand(producto_id=products[0], cantidad=3),
                    LineCommand(producto_id=products[1], cantidad=2),
                ],
            )
        )
        RefundSale(factory).execute(
            sale.id,
            RefundCommand(
                motivo_id=root.motivo_repo.list()[0].id,
                metodo_reintegro_id=root.metodo_pago_repo.list()[0].id,
                detalle="Ejemplo de devolución parcial apta para reventa.",
                productos_aptos=True,
                detalles=[LineCommand(producto_id=products[0], cantidad=1)],
            ),
        )
        order2 = CreateReplenishmentOrder(factory).execute(
            OrderCommand(
                establecimiento_solicitante_id=north,
                establecimiento_proveedor_id=cd,
                detalles=[LineCommand(producto_id=products[0], cantidad=8)],
            )
        )
        delivery2 = CreateDelivery(factory).execute(order2.id, "R-DEMO-002")
        package = PreparePackage(factory).execute(
            delivery2.id,
            PackageCommand(
                responsable="Ana Demo",
                detalles=[LineCommand(producto_id=products[0], cantidad=8)],
            ),
        )
        TransitionPackage(factory).execute(
            package.id,
            "precintar",
            TransitionCommand(responsable="Ana Demo", codigo_precinto="P-DEMO-3"),
        )
        TransitionPackage(factory).execute(
            package.id, "despachar", TransitionCommand(responsable="Ana Demo")
        )
        TransitionPackage(factory).execute(
            package.id, "recibir", TransitionCommand(responsable="Luis Demo")
        )
        TransitionPackage(factory).execute(
            package.id,
            "inspeccionar",
            TransitionCommand(
                responsable="Luis Demo",
                codigo_precinto="P-DEMO-3",
                numero_remito="R-DEMO-002",
                precinto_intacto=False,
                contenido_conforme=True,
                observacion="Precinto roto al recibir (ejemplo).",
            ),
        )
