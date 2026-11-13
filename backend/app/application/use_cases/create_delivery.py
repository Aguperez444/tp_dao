from __future__ import annotations

from app.application.dto.response.remito_object_response import RemitoObjectResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.clock_service import now
from app.application.services.entity_validation_service import EntityValidationService
from app.application.services.logistics_service import LogisticsService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.remito import Remito


class CreateDelivery:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, order_id: int, number: str) -> RemitoObjectResponse:
        number = number.strip().upper()
        if not number:
            raise BusinessError("Indique el número del remito.")
        with self.uow_factory(write=True) as uow:
            EntityValidationService.require(uow.orden_reposicion_repo, order_id)
            if any(
                (
                    EntityValidationService.state_name(
                        uow.estado_remito_repo, delivery.estado_remito_id
                    )
                    == "Pendiente"
                    for delivery in uow.remito_repo.list(orden_reposicion_id=order_id)
                )
            ):
                raise BusinessError(
                    "Complete la preparación e inicie el despacho del remito pendiente antes de generar otro."
                )
            requested = {
                x.producto_id: x.cantidad
                for x in uow.detalle_reposicion_repo.list(orden_id=order_id)
            }
            allocated = LogisticsService.allocated(uow, order_id)
            if all((allocated.get(p, 0) >= q for p, q in requested.items())):
                raise BusinessError(
                    "La orden ya tiene toda la mercadería asignada a bultos."
                )
            return RemitoObjectResponse.from_entity(
                uow.remito_repo.save(
                    Remito(
                        orden_reposicion_id=order_id,
                        numero_remito=number,
                        fecha_emision=now(),
                        estado_remito_id=EntityValidationService.state_id(
                            uow.estado_remito_repo, "Pendiente"
                        ),
                    )
                )
            )
