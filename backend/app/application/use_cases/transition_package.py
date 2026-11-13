from app.application.dto.commands.transition_command import TransitionCommand
from app.application.dto.response.package_transition_response import (
    PackageTransitionResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.entity_validation_service import EntityValidationService
from app.application.services.logistics_service import LogisticsService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.package import Package
from app.domain.services.shipping.state_factory import STATES


class TransitionPackage:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, id: int, action: str, data: TransitionCommand
    ) -> PackageTransitionResponse:
        with self.uow_factory(write=True) as uow:
            package = EntityValidationService.require(uow.bulto_repo, id)
            delivery = EntityValidationService.require(
                uow.remito_repo, package.remito_id
            )
            order = EntityValidationService.require(
                uow.orden_reposicion_repo, delivery.orden_reposicion_id
            )
            state_name = EntityValidationService.state_name(
                uow.estado_bulto_repo, package.estado_bulto_id
            )
            note = data.observacion.strip()
            if action == "inspeccionar":
                seal = data.codigo_precinto.strip().upper()
                same_seal = seal == package.codigo_precinto
                same_delivery = (
                    data.numero_remito.strip().upper() == delivery.numero_remito
                )
                intact = data.precinto_intacto is True
                conforming = data.contenido_conforme is True
                valid = same_seal and same_delivery and intact and conforming
                action = "verificar" if valid else "rechazar"
                if not valid and not note:
                    raise BusinessError("Explique el motivo del rechazo.")
                seal_state = (
                    "Violado"
                    if not intact
                    else ("No coincide" if not same_seal else "Intacto")
                )
                package.estado_precinto_id = EntityValidationService.state_id(
                    uow.estado_precinto_repo, seal_state
                )
            elif action in ("verificar", "rechazar"):
                raise BusinessError(
                    "El resultado se obtiene inspeccionando el precinto y el remito."
                )
            new_state = Package(STATES[state_name]()).execute(action)
            if action == "precintar":
                seal = data.codigo_precinto.strip().upper()
                if not seal:
                    raise BusinessError("Debe registrar un código de precinto único.")
                package.codigo_precinto = seal
                package.estado_precinto_id = EntityValidationService.state_id(
                    uow.estado_precinto_repo, "Intacto"
                )
            if action == "despachar":
                packages = uow.bulto_repo.list(remito_id=delivery.id)
                if any(
                    EntityValidationService.state_name(
                        uow.estado_bulto_repo, item.estado_bulto_id
                    )
                    == "Preparado"
                    for item in packages
                ):
                    raise BusinessError(
                        "Precinte todos los bultos del remito antes del primer despacho."
                    )
                for line in uow.detalle_bulto_repo.list(bulto_id=id):
                    stock = uow.existencia_repo.stock(
                        order.establecimiento_proveedor_id, line.producto_id
                    )
                    stock.almacenado_total -= line.cantidad
                    stock.reservado -= line.cantidad
                    uow.existencia_repo.update(stock)
            package.estado_bulto_id = EntityValidationService.state_id(
                uow.estado_bulto_repo, new_state
            )
            uow.bulto_repo.update(package)
            LogisticsService.event(
                uow, id, new_state, data.responsable, note or action.capitalize()
            )
            LogisticsService.refresh_delivery(uow, delivery)
            LogisticsService.refresh_order(uow, order.id)
            return PackageTransitionResponse.from_entity(
                EntityValidationService.require(uow.bulto_repo, id), estado=new_state
            )
