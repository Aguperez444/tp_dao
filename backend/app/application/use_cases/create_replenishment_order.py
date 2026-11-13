from __future__ import annotations

from app.application.dto.commands.order_command import OrderCommand
from app.application.dto.response.orden_reposicion_object_response import (
    OrdenReposicionObjectResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.clock_service import now
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.models.detalle_reposicion import DetalleReposicion
from app.domain.models.orden_reposicion import OrdenReposicion


class CreateReplenishmentOrder:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, data: OrderCommand) -> OrdenReposicionObjectResponse:
        with self.uow_factory(write=True) as uow:
            EntityValidationService.local(
                uow.establecimiento_repo, data.establecimiento_solicitante_id
            )
            EntityValidationService.local(
                uow.establecimiento_repo,
                data.establecimiento_proveedor_id,
                central=True,
            )
            lines = EntityValidationService.lines(uow.producto_repo, data.detalles)
            order = uow.orden_reposicion_repo.save(
                OrdenReposicion(
                    establecimiento_solicitante_id=data.establecimiento_solicitante_id,
                    establecimiento_proveedor_id=data.establecimiento_proveedor_id,
                    fecha=now(),
                    estado_id=EntityValidationService.state_id(
                        uow.estado_reposicion_repo, "Pendiente"
                    ),
                )
            )
            for product, quantity in lines.items():
                uow.detalle_reposicion_repo.save(
                    DetalleReposicion(
                        orden_id=order.id, producto_id=product, cantidad=quantity
                    )
                )
            return OrdenReposicionObjectResponse.from_entity(order)
