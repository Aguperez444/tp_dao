from app.domain.models.detalle_devolucion import DetalleDevolucion
from app.infrastructure.database.models.detalle_devolucion_orm import (
    DetalleDevolucionORM,
)


class DetalleDevolucionMapper:
    @staticmethod
    def orm_to_domain(instance: DetalleDevolucionORM) -> DetalleDevolucion:
        return DetalleDevolucion(
            id=instance.id,
            producto_id=instance.producto_id,
            devolucion_id=instance.devolucion_id,
            cantidad=instance.cantidad,
            importe_unitario=instance.importe_unitario,
        )

    @staticmethod
    def domain_to_orm(entity: DetalleDevolucion) -> DetalleDevolucionORM:
        return DetalleDevolucionORM(
            id=entity.id if entity.is_persisted() else None,
            producto_id=entity.producto_id,
            devolucion_id=entity.devolucion_id,
            cantidad=entity.cantidad,
            importe_unitario=entity.importe_unitario,
        )
