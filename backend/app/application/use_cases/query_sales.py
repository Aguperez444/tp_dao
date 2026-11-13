from __future__ import annotations

from app.application.dto.response.sale_summary_response import SaleSummaryResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.entity_validation_service import EntityValidationService


class QuerySales:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self) -> list[SaleSummaryResponse]:
        with self.uow_factory() as uow:
            return [
                SaleSummaryResponse.from_entity(
                    sale,
                    local=EntityValidationService.require(
                        uow.establecimiento_repo, sale.local_id
                    ).nombre,
                    metodo_pago=EntityValidationService.require(
                        uow.metodo_pago_repo, sale.metodo_pago_id
                    ).nombre,
                    reintegrado=sum(
                        (
                            line.cantidad * line.importe_unitario
                            for refund in uow.devolucion_repo.list(venta_id=sale.id)
                            for line in uow.detalle_devolucion_repo.list(
                                devolucion_id=refund.id
                            )
                        )
                    ),
                )
                for sale in uow.venta_repo.list()
            ][::-1]
