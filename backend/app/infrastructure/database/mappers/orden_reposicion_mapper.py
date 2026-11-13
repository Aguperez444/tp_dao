from app.domain.models.orden_reposicion import OrdenReposicion
from app.infrastructure.database.models.orden_reposicion_orm import OrdenReposicionORM


class OrdenReposicionMapper:
    @staticmethod
    def orm_to_domain(instance: OrdenReposicionORM) -> OrdenReposicion:
        return OrdenReposicion(
            id=instance.id,
            establecimiento_solicitante_id=instance.establecimiento_solicitante_id,
            establecimiento_proveedor_id=instance.establecimiento_proveedor_id,
            fecha=instance.fecha,
            estado_id=instance.estado_id,
        )

    @staticmethod
    def domain_to_orm(entity: OrdenReposicion) -> OrdenReposicionORM:
        return OrdenReposicionORM(
            id=entity.id if entity.is_persisted() else None,
            establecimiento_solicitante_id=entity.establecimiento_solicitante_id,
            establecimiento_proveedor_id=entity.establecimiento_proveedor_id,
            fecha=entity.fecha,
            estado_id=entity.estado_id,
        )
