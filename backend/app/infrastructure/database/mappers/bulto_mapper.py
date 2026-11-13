from app.domain.models.bulto import Bulto
from app.infrastructure.database.models.bulto_orm import BultoORM


class BultoMapper:
    @staticmethod
    def orm_to_domain(instance: BultoORM) -> Bulto:
        return Bulto(
            id=instance.id,
            remito_id=instance.remito_id,
            estado_precinto_id=instance.estado_precinto_id,
            estado_bulto_id=instance.estado_bulto_id,
            codigo_precinto=instance.codigo_precinto,
        )

    @staticmethod
    def domain_to_orm(entity: Bulto) -> BultoORM:
        return BultoORM(
            id=entity.id if entity.is_persisted() else None,
            remito_id=entity.remito_id,
            estado_precinto_id=entity.estado_precinto_id,
            estado_bulto_id=entity.estado_bulto_id,
            codigo_precinto=entity.codigo_precinto,
        )
