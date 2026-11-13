from __future__ import annotations

from app.application.dto.response.compra_object_response import CompraObjectResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.clock_service import now
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.exceptions.business_error import BusinessError


class ReceivePurchase:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, id: int) -> CompraObjectResponse:
        with self.uow_factory(write=True) as uow:
            purchase = EntityValidationService.require(uow.compra_repo, id)
            if (
                EntityValidationService.state_name(
                    uow.estado_compra_repo, purchase.estado_id
                )
                != "Pendiente"
            ):
                raise BusinessError(
                    "La compra ya fue recibida; no se puede acreditar nuevamente."
                )
            cd = EntityValidationService.central(uow.establecimiento_repo)
            for line in uow.detalle_compra_repo.list(compra_id=id):
                stock = uow.existencia_repo.stock(cd.id, line.producto_id)
                stock.almacenado_total = stock.almacenado_total + line.cantidad
                uow.existencia_repo.update(stock)
            purchase.estado_id = EntityValidationService.state_id(
                uow.estado_compra_repo, "Recibida"
            )
            purchase.fecha = now()
            return CompraObjectResponse.from_entity(uow.compra_repo.update(purchase))
