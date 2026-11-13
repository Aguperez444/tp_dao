from app.domain.models.estado_precinto import EstadoPrecinto
from app.infrastructure.database.models.estado_precinto_orm import EstadoPrecintoORM


class EstadoPrecintoMapper:
    @staticmethod
    def orm_to_domain(instance: EstadoPrecintoORM) -> EstadoPrecinto:
        return EstadoPrecinto(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: EstadoPrecinto) -> EstadoPrecintoORM:
        return EstadoPrecintoORM(
            id=entity.id if entity.is_persisted() else None, nombre=entity.nombre
        )
