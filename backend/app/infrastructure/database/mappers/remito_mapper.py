from app.domain.models.remito import Remito
from app.infrastructure.database.models.remito_orm import RemitoORM


class RemitoMapper:
    @staticmethod
    def orm_to_domain(instance: RemitoORM) -> Remito:
        return Remito(
            id=instance.id,
            orden_reposicion_id=instance.orden_reposicion_id,
            estado_remito_id=instance.estado_remito_id,
            numero_remito=instance.numero_remito,
            fecha_emision=instance.fecha_emision,
        )

    @staticmethod
    def domain_to_orm(entity: Remito) -> RemitoORM:
        orm = RemitoORM(
            orden_reposicion_id=entity.orden_reposicion_id,
            estado_remito_id=entity.estado_remito_id,
            numero_remito=entity.numero_remito,
            fecha_emision=entity.fecha_emision,
        )
        if entity.id is not None:
            orm.id = entity.id
        return orm
