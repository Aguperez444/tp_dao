from __future__ import annotations

from app.application.dto.commands.purchase_command import PurchaseCommand
from app.application.dto.response.compra_object_response import CompraObjectResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.clock_service import now
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.models.compra import Compra
from app.domain.models.detalle_compra import DetalleCompra
from app.domain.services.money_service import to_cents


class CreatePurchase:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, data: PurchaseCommand) -> CompraObjectResponse:
        with self.uow_factory(write=True) as uow:
            EntityValidationService.central(uow.establecimiento_repo)
            EntityValidationService.require(uow.proveedor_repo, data.proveedor_id)
            EntityValidationService.lines(uow.producto_repo, data.detalles)
            purchase = uow.compra_repo.save(
                Compra(
                    proveedor_id=data.proveedor_id,
                    estado_id=EntityValidationService.state_id(
                        uow.estado_compra_repo, "Pendiente"
                    ),
                    fecha=now(),
                )
            )
            for line in data.detalles:
                uow.detalle_compra_repo.save(
                    DetalleCompra(
                        compra_id=purchase.id,
                        producto_id=line.producto_id,
                        cantidad=line.cantidad,
                        costo=to_cents(line.costo),
                    )
                )
            return CompraObjectResponse.from_entity(purchase)
