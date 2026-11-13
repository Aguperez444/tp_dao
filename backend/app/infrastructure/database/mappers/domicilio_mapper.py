from app.domain.models.domicilio import Domicilio
from app.infrastructure.database.models.domicilio_orm import DomicilioORM


class DomicilioMapper:
    @staticmethod
    def orm_to_domain(instance: DomicilioORM) -> Domicilio:
        return Domicilio(
            id=instance.id,
            calle=instance.calle,
            altura=instance.altura,
            ciudad_id=instance.ciudad_id,
        )

    @staticmethod
    def domain_to_orm(entity: Domicilio) -> DomicilioORM:
        return DomicilioORM(
            id=entity.id if entity.is_persisted() else None,
            calle=entity.calle,
            altura=entity.altura,
            ciudad_id=entity.ciudad_id,
        )
