from __future__ import annotations

from app.application.dto.commands.sale_command import SaleCommand
from app.application.dto.response.sale_detail_response import SaleDetailResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.clock_service import now
from app.application.services.entity_validation_service import EntityValidationService
from app.application.services.sale_detail_service import SaleDetailService
from app.application.services.sale_pricing_service import SalePricingService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.venta import Venta
from app.domain.services.money_service import to_cents


class CreateSale:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, data: SaleCommand) -> SaleDetailResponse:
        with self.uow_factory(write=True) as uow:
            EntityValidationService.require(uow.metodo_pago_repo, data.metodo_pago_id)
            quote = SalePricingService.quote(uow, data)
            if to_cents(data.importe_cobrado) != quote.total:
                raise BusinessError(
                    f"El cobro debe coincidir con el total vigente: ${quote.total / 100:.2f}. Revise los precios antes de confirmar."
                )
            sale = uow.venta_repo.save(
                Venta(
                    local_id=data.local_id,
                    metodo_pago_id=data.metodo_pago_id,
                    total=quote.total,
                    fecha=now(),
                    numero_comprobante="V-PROVISIONAL",
                )
            )
            sale.numero_comprobante = f"V-{sale.id:08d}"
            uow.venta_repo.update(sale)
            for line in quote.detalles:
                uow.detalle_venta_repo.save(
                    DetalleVenta(
                        producto_id=line.producto_id,
                        cantidad=line.cantidad,
                        precio_unitario=line.precio_unitario,
                        descuento_aplicado=line.descuento_aplicado,
                        costo_unitario=line.costo_unitario,
                        venta_id=sale.id,
                    )
                )
                stock = uow.existencia_repo.stock(data.local_id, line.producto_id)
                stock.almacenado_total = stock.almacenado_total - line.cantidad
                uow.existencia_repo.update(stock)
            return SaleDetailService.get(uow, sale.id)
