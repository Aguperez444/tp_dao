from __future__ import annotations

from app.application.dto.response.detalle_devolucion_object_response import (
    DetalleDevolucionObjectResponse,
)
from app.application.dto.response.refund_detail_response import RefundDetailResponse
from app.application.dto.response.sale_detail_line_response import (
    SaleDetailLineResponse,
)
from app.application.dto.response.sale_detail_response import SaleDetailResponse
from app.application.ports.i_unit_of_work import IUnitOfWork
from app.application.services.entity_validation_service import EntityValidationService


class SaleDetailService:
    @staticmethod
    def get(uow: IUnitOfWork, id: int) -> SaleDetailResponse:
        sale = EntityValidationService.require(uow.venta_repo, id)
        details = [
            SaleDetailLineResponse.from_entity(
                line,
                producto=EntityValidationService.require(
                    uow.producto_repo, line.producto_id, active=False
                ).nombre,
                devuelta=uow.detalle_devolucion_repo.returned(id, line.producto_id),
                subtotal=line.cantidad
                * (line.precio_unitario - line.descuento_aplicado),
            )
            for line in uow.detalle_venta_repo.list(venta_id=id)
        ]
        refunds = []
        for refund in uow.devolucion_repo.list(venta_id=id):
            lines = uow.detalle_devolucion_repo.list(devolucion_id=refund.id)
            refunds.append(
                RefundDetailResponse.from_entity(
                    refund,
                    numero_comprobante=f"D-{refund.id:08d}",
                    motivo=EntityValidationService.require(
                        uow.motivo_repo, refund.motivo_id
                    ).nombre,
                    metodo_reintegro=EntityValidationService.require(
                        uow.metodo_pago_repo, refund.metodo_reintegro_id
                    ).nombre,
                    total=sum(
                        (line.cantidad * line.importe_unitario for line in lines)
                    ),
                    detalles=[
                        DetalleDevolucionObjectResponse.from_entity(item)
                        for item in lines
                    ],
                )
            )
        return SaleDetailResponse.from_entity(
            sale,
            local=EntityValidationService.require(
                uow.establecimiento_repo, sale.local_id
            ).nombre,
            metodo_pago=EntityValidationService.require(
                uow.metodo_pago_repo, sale.metodo_pago_id
            ).nombre,
            detalles=details,
            devoluciones=refunds,
            reintegrado=sum((refund.total for refund in refunds)),
        )
