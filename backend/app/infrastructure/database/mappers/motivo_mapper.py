from app.domain.models.motivo import Motivo
from app.infrastructure.database.models.motivo_orm import MotivoORM


class MotivoMapper:
    @staticmethod
    def orm_to_domain(instance: MotivoORM) -> Motivo:
        return Motivo(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: Motivo) -> MotivoORM:
        return MotivoORM(
            id=entity.id if entity.is_persisted() else None, nombre=entity.nombre
        )
