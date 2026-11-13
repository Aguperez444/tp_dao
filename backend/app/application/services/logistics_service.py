from __future__ import annotations

from app.application.ports.i_unit_of_work import IUnitOfWork
from app.application.services.clock_service import now
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.cambio_estado_bulto import CambioEstadoBulto
from app.domain.models.remito import Remito


class LogisticsService:
    """Asignación e historial de bultos dentro de la transacción del caso de uso."""

    @staticmethod
    def allocated(uow: IUnitOfWork, order_id: int) -> dict[int, int]:
        quantities = {}
        for delivery in uow.remito_repo.list(orden_reposicion_id=order_id):
            for package in uow.bulto_repo.list(remito_id=delivery.id):
                for line in uow.detalle_bulto_repo.list(bulto_id=package.id):
                    p = line.producto_id
                    quantities[p] = quantities.get(p, 0) + line.cantidad
        return quantities

    @staticmethod
    def event(
        uow: IUnitOfWork, id: int, state: str, responsible: str, note: str
    ) -> None:
        responsible = responsible.strip()
        if not responsible:
            raise BusinessError("Identifique al responsable de la operación.")
        uow.cambio_estado_bulto_repo.save(
            CambioEstadoBulto(
                bulto_id=id,
                estado_bulto_id=EntityValidationService.state_id(
                    uow.estado_bulto_repo, state
                ),
                fecha=now(),
                responsable=responsible,
                observacion=note,
            )
        )

    @staticmethod
    def refresh_delivery(uow: IUnitOfWork, delivery: Remito) -> None:
        packages = uow.bulto_repo.list(remito_id=delivery.id)
        states = [
            EntityValidationService.state_name(uow.estado_bulto_repo, p.estado_bulto_id)
            for p in packages
        ]
        old_state = EntityValidationService.state_name(
            uow.estado_remito_repo, delivery.estado_remito_id
        )
        if old_state in ("Verificado", "Rechazado"):
            return
        if "Rechazado" in states:
            new_state = "Rechazado"
        elif all((s == "Verificado" for s in states)):
            new_state = "Verificado"
            order = EntityValidationService.require(
                uow.orden_reposicion_repo, delivery.orden_reposicion_id
            )
            for package in packages:
                for line in uow.detalle_bulto_repo.list(bulto_id=package.id):
                    stock = uow.existencia_repo.stock(
                        order.establecimiento_solicitante_id, line.producto_id
                    )
                    stock.almacenado_total = stock.almacenado_total + line.cantidad
                    uow.existencia_repo.update(stock)
        elif all((s in ("Recibido", "Verificado") for s in states)):
            new_state = "Recibido"
        elif any((s in ("En tránsito", "Recibido", "Verificado") for s in states)):
            new_state = "En tránsito"
        else:
            new_state = "Pendiente"
        delivery.estado_remito_id = EntityValidationService.state_id(
            uow.estado_remito_repo, new_state
        )
        uow.remito_repo.update(delivery)

    @staticmethod
    def refresh_order(uow: IUnitOfWork, id: int) -> None:
        order = EntityValidationService.require(uow.orden_reposicion_repo, id)
        deliveries = uow.remito_repo.list(orden_reposicion_id=id)
        states = [
            EntityValidationService.state_name(
                uow.estado_remito_repo, d.estado_remito_id
            )
            for d in deliveries
        ]
        allocated = LogisticsService.allocated(uow, id)
        all_allocated = all(
            (
                allocated.get(x.producto_id, 0) == x.cantidad
                for x in uow.detalle_reposicion_repo.list(orden_id=id)
            )
        )
        if all_allocated and states and all((s == "Verificado" for s in states)):
            state = "Completada"
        elif "Rechazado" in states:
            state = "Con rechazos"
        elif any((s in ("En tránsito", "Recibido", "Verificado") for s in states)):
            state = "En tránsito"
        elif allocated:
            state = "En preparación"
        else:
            state = "Pendiente"
        order.estado_id = EntityValidationService.state_id(
            uow.estado_reposicion_repo, state
        )
        uow.orden_reposicion_repo.update(order)
