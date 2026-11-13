from __future__ import annotations

from app.application.dto.commands.package_command import PackageCommand
from app.application.dto.response.bulto_object_response import BultoObjectResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.entity_validation_service import EntityValidationService
from app.application.services.logistics_service import LogisticsService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.bulto import Bulto
from app.domain.models.detalle_bulto import DetalleBulto


class PreparePackage:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, delivery_id: int, data: PackageCommand) -> BultoObjectResponse:
        with self.uow_factory(write=True) as uow:
            delivery = EntityValidationService.require(uow.remito_repo, delivery_id)
            if (
                EntityValidationService.state_name(
                    uow.estado_remito_repo, delivery.estado_remito_id
                )
                != "Pendiente"
            ):
                raise BusinessError(
                    "El remito ya inició su despacho y no admite más bultos."
                )
            order = EntityValidationService.require(
                uow.orden_reposicion_repo, delivery.orden_reposicion_id
            )
            requested = {
                x.producto_id: x.cantidad
                for x in uow.detalle_reposicion_repo.list(orden_id=order.id)
            }
            allocated = LogisticsService.allocated(uow, order.id)
            lines = EntityValidationService.lines(uow.producto_repo, data.detalles)
            for p, q in lines.items():
                if allocated.get(p, 0) + q > requested.get(p, 0):
                    raise BusinessError(
                        "El bulto excede lo solicitado o incluye un producto ajeno a la orden."
                    )
                stock = uow.existencia_repo.stock(order.establecimiento_proveedor_id, p)
                if stock.almacenado_total - stock.reservado < q:
                    raise BusinessError("No hay stock disponible suficiente en el CD.")
                stock.reservado = stock.reservado + q
                uow.existencia_repo.update(stock)
            package = uow.bulto_repo.save(
                Bulto(
                    remito_id=delivery_id,
                    estado_precinto_id=EntityValidationService.state_id(
                        uow.estado_precinto_repo, "Sin colocar"
                    ),
                    estado_bulto_id=EntityValidationService.state_id(
                        uow.estado_bulto_repo, "Preparado"
                    ),
                    codigo_precinto=None,
                )
            )
            for p, q in lines.items():
                uow.detalle_bulto_repo.save(
                    DetalleBulto(bulto_id=package.id, producto_id=p, cantidad=q)
                )
            LogisticsService.event(
                uow,
                package.id,
                "Preparado",
                data.responsable,
                "Mercadería reservada en el CD.",
            )
            LogisticsService.refresh_order(uow, order.id)
            return BultoObjectResponse.from_entity(package)
