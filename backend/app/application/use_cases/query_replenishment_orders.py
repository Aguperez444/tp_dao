from __future__ import annotations

from app.application.dto.response.delivery_detail_response import DeliveryDetailResponse
from app.application.dto.response.detalle_bulto_object_response import (
    DetalleBultoObjectResponse,
)
from app.application.dto.response.package_detail_response import PackageDetailResponse
from app.application.dto.response.package_event_response import PackageEventResponse
from app.application.dto.response.replenishment_line_response import (
    ReplenishmentLineResponse,
)
from app.application.dto.response.replenishment_order_response import (
    ReplenishmentOrderResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.entity_validation_service import EntityValidationService
from app.application.services.logistics_service import LogisticsService


class QueryReplenishmentOrders:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self) -> list[ReplenishmentOrderResponse]:
        with self.uow_factory() as uow:
            rows = []
            for order in uow.orden_reposicion_repo.list():
                lines = uow.detalle_reposicion_repo.list(orden_id=order.id)
                allocated = LogisticsService.allocated(uow, order.id)
                deliveries = []
                for delivery in uow.remito_repo.list(orden_reposicion_id=order.id):
                    packages = []
                    for package in uow.bulto_repo.list(remito_id=delivery.id):
                        history = [
                            PackageEventResponse.from_entity(
                                ev,
                                estado=EntityValidationService.state_name(
                                    uow.estado_bulto_repo, ev.estado_bulto_id
                                ),
                            )
                            for ev in uow.cambio_estado_bulto_repo.list(
                                bulto_id=package.id
                            )
                        ]
                        packages.append(
                            PackageDetailResponse.from_entity(
                                package,
                                estado=EntityValidationService.state_name(
                                    uow.estado_bulto_repo, package.estado_bulto_id
                                ),
                                estado_precinto=EntityValidationService.state_name(
                                    uow.estado_precinto_repo, package.estado_precinto_id
                                ),
                                detalles=[
                                    DetalleBultoObjectResponse.from_entity(item)
                                    for item in uow.detalle_bulto_repo.list(
                                        bulto_id=package.id
                                    )
                                ],
                                historial=history,
                            )
                        )
                    deliveries.append(
                        DeliveryDetailResponse.from_entity(
                            delivery,
                            estado=EntityValidationService.state_name(
                                uow.estado_remito_repo, delivery.estado_remito_id
                            ),
                            bultos=packages,
                        )
                    )
                rows.append(
                    ReplenishmentOrderResponse.from_entity(
                        order,
                        origen=EntityValidationService.require(
                            uow.establecimiento_repo, order.establecimiento_proveedor_id
                        ).nombre,
                        destino=EntityValidationService.require(
                            uow.establecimiento_repo,
                            order.establecimiento_solicitante_id,
                        ).nombre,
                        estado=EntityValidationService.state_name(
                            uow.estado_reposicion_repo, order.estado_id
                        ),
                        detalles=[
                            ReplenishmentLineResponse.from_entity(
                                line, asignada=allocated.get(line.producto_id, 0)
                            )
                            for line in lines
                        ],
                        remitos=deliveries,
                    )
                )
            return rows[::-1]
