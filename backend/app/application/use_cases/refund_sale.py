from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.application.dto.commands.refund_command import RefundCommand
from app.application.dto.commands.refund_line import RefundLine
from app.application.dto.response.sale_detail_response import SaleDetailResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.clock_service import now
from app.application.services.entity_validation_service import EntityValidationService
from app.application.services.sale_detail_service import SaleDetailService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.detalle_devolucion import DetalleDevolucion
from app.domain.models.devolucion import Devolucion


class RefundSale:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, id: int, data: RefundCommand) -> SaleDetailResponse:
        if data.productos_aptos is not True:
            raise BusinessError(
                "Esta devolución requiere productos inspeccionados y aptos para reventa."
            )
        with self.uow_factory(write=True) as uow:
            sale = EntityValidationService.require(uow.venta_repo, id)
            if datetime.now(timezone.utc) - datetime.fromisoformat(
                sale.fecha
            ) > timedelta(days=30):
                raise BusinessError(
                    "La venta superó el plazo de devolución de 30 días."
                )
            EntityValidationService.require(uow.motivo_repo, data.motivo_id)
            EntityValidationService.require(
                uow.metodo_pago_repo, data.metodo_reintegro_id
            )
            original = {
                line.producto_id: line
                for line in uow.detalle_venta_repo.list(venta_id=id)
            }
            if not data.detalles:
                raise BusinessError("Seleccione productos a devolver.")
            checked, seen = ([], set())
            for line in data.detalles:
                product, quantity = (line.producto_id, line.cantidad)
                if type(quantity) is not int or quantity <= 0 or product in seen:
                    raise BusinessError(
                        "Use cantidades enteras positivas y no repita productos."
                    )
                seen.add(product)
                if (
                    product not in original
                    or uow.detalle_devolucion_repo.returned(id, product) + quantity
                    > original[product].cantidad
                ):
                    raise BusinessError(
                        "La devolución no corresponde a la venta o supera la cantidad pendiente."
                    )
                unit = (
                    original[product].precio_unitario
                    - original[product].descuento_aplicado
                )
                checked.append(
                    RefundLine(
                        producto_id=product, cantidad=quantity, importe_unitario=unit
                    )
                )
            refund = uow.devolucion_repo.save(
                Devolucion(
                    venta_id=id,
                    motivo_id=data.motivo_id,
                    metodo_reintegro_id=data.metodo_reintegro_id,
                    detalle=data.detalle.strip(),
                    fecha=now(),
                )
            )
            for line in checked:
                uow.detalle_devolucion_repo.save(
                    DetalleDevolucion(
                        producto_id=line.producto_id,
                        cantidad=line.cantidad,
                        importe_unitario=line.importe_unitario,
                        devolucion_id=refund.id,
                    )
                )
                stock = uow.existencia_repo.stock(sale.local_id, line.producto_id)
                stock.almacenado_total = stock.almacenado_total + line.cantidad
                uow.existencia_repo.update(stock)
            return SaleDetailService.get(uow, id)
