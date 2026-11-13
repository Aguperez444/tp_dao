from app.domain.models.estado_bulto import EstadoBulto
from app.infrastructure.database.models.estado_bulto_orm import EstadoBultoORM


class EstadoBultoMapper:
    @staticmethod
    def orm_to_domain(instance: EstadoBultoORM) -> EstadoBulto:
        return EstadoBulto(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: EstadoBulto) -> EstadoBultoORM:
        return EstadoBultoORM(
            id=entity.id if entity.is_persisted() else None, nombre=entity.nombre
        )
