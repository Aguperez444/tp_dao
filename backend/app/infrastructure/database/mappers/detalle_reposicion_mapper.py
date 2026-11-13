from app.domain.models.detalle_reposicion import DetalleReposicion
from app.infrastructure.database.models.detalle_reposicion_orm import (
    DetalleReposicionORM,
)


class DetalleReposicionMapper:
    @staticmethod
    def orm_to_domain(instance: DetalleReposicionORM) -> DetalleReposicion:
        return DetalleReposicion(
            id=instance.id,
            producto_id=instance.producto_id,
            orden_id=instance.orden_id,
            cantidad=instance.cantidad,
        )

    @staticmethod
    def domain_to_orm(entity: DetalleReposicion) -> DetalleReposicionORM:
        orm = DetalleReposicionORM(
            producto_id=entity.producto_id,
            orden_id=entity.orden_id,
            cantidad=entity.cantidad,
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm