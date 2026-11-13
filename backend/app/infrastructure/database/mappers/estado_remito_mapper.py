from app.domain.models.estado_remito import EstadoRemito
from app.infrastructure.database.models.estado_remito_orm import EstadoRemitoORM


class EstadoRemitoMapper:
    @staticmethod
    def orm_to_domain(instance: EstadoRemitoORM) -> EstadoRemito:
        return EstadoRemito(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: EstadoRemito) -> EstadoRemitoORM:
        orm = EstadoRemitoORM(
            nombre=entity.nombre
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
