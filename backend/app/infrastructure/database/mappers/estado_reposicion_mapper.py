from app.domain.models.estado_reposicion import EstadoReposicion
from app.infrastructure.database.models.estado_reposicion_orm import EstadoReposicionORM


class EstadoReposicionMapper:
    @staticmethod
    def orm_to_domain(instance: EstadoReposicionORM) -> EstadoReposicion:
        return EstadoReposicion(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: EstadoReposicion) -> EstadoReposicionORM:
        orm = EstadoReposicionORM(
            nombre=entity.nombre
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
