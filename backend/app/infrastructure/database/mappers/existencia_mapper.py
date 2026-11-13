from app.domain.models.existencia import Existencia
from app.infrastructure.database.models.existencia_orm import ExistenciaORM


class ExistenciaMapper:
    @staticmethod
    def orm_to_domain(instance: ExistenciaORM) -> Existencia:
        return Existencia(
            id=instance.id,
            establecimiento_id=instance.establecimiento_id,
            producto_id=instance.producto_id,
            almacenado_total=instance.almacenado_total,
            reservado=instance.reservado,
            minimo_permitido=instance.minimo_permitido,
        )

    @staticmethod
    def domain_to_orm(entity: Existencia) -> ExistenciaORM:
        return ExistenciaORM(
            id=entity.id if entity.is_persisted() else None,
            establecimiento_id=entity.establecimiento_id,
            producto_id=entity.producto_id,
            almacenado_total=entity.almacenado_total,
            reservado=entity.reservado,
            minimo_permitido=entity.minimo_permitido,
        )
