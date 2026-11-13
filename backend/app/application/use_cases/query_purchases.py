from __future__ import annotations

from app.application.dto.response.detalle_compra_object_response import (
    DetalleCompraObjectResponse,
)
from app.application.dto.response.purchase_summary_response import (
    PurchaseSummaryResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.entity_validation_service import EntityValidationService


class QueryPurchases:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self) -> list[PurchaseSummaryResponse]:
        with self.uow_factory() as uow:
            results = []
            for purchase in uow.compra_repo.list():
                lines = uow.detalle_compra_repo.list(compra_id=purchase.id)
                results.append(
                    PurchaseSummaryResponse.from_entity(
                        purchase,
                        estado=EntityValidationService.state_name(
                            uow.estado_compra_repo, purchase.estado_id
                        ),
                        proveedor=EntityValidationService.require(
                            uow.proveedor_repo, purchase.proveedor_id, active=False
                        ).nombre,
                        total=sum((x.cantidad * x.costo for x in lines)),
                        detalles=[
                            DetalleCompraObjectResponse.from_entity(item)
                            for item in lines
                        ],
                    )
                )
            return results[::-1]
