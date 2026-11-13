from app.domain.models.estado_bulto import EstadoBulto
from app.infrastructure.database.models.estado_bulto_orm import EstadoBultoORM


class EstadoBultoMapper:
    @staticmethod
    def orm_to_domain(instance: EstadoBultoORM) -> EstadoBulto:
        return EstadoBulto(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: EstadoBulto) -> EstadoBultoORM:
        orm = EstadoBultoORM(
            nombre=entity.nombre
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
