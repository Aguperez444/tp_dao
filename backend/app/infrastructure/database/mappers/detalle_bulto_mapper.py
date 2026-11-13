from app.domain.models.detalle_bulto import DetalleBulto
from app.infrastructure.database.models.detalle_bulto_orm import DetalleBultoORM


class DetalleBultoMapper:
    @staticmethod
    def orm_to_domain(instance: DetalleBultoORM) -> DetalleBulto:
        return DetalleBulto(
            id=instance.id,
            producto_id=instance.producto_id,
            bulto_id=instance.bulto_id,
            cantidad=instance.cantidad,
        )

    @staticmethod
    def domain_to_orm(entity: DetalleBulto) -> DetalleBultoORM:
        orm =  DetalleBultoORM(
            producto_id=entity.producto_id,
            bulto_id=entity.bulto_id,
            cantidad=entity.cantidad,
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
