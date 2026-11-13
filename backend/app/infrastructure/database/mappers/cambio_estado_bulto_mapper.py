from app.domain.models.cambio_estado_bulto import CambioEstadoBulto
from app.infrastructure.database.models.cambio_estado_bulto_orm import (
    CambioEstadoBultoORM,
)


class CambioEstadoBultoMapper:
    @staticmethod
    def orm_to_domain(instance: CambioEstadoBultoORM) -> CambioEstadoBulto:
        return CambioEstadoBulto(
            id=instance.id,
            bulto_id=instance.bulto_id,
            estado_bulto_id=instance.estado_bulto_id,
            fecha=instance.fecha,
            responsable=instance.responsable,
            observacion=instance.observacion,
        )

    @staticmethod
    def domain_to_orm(entity: CambioEstadoBulto) -> CambioEstadoBultoORM:
        orm = CambioEstadoBultoORM(
            bulto_id=entity.bulto_id,
            estado_bulto_id=entity.estado_bulto_id,
            fecha=entity.fecha,
            responsable=entity.responsable,
            observacion=entity.observacion,
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
