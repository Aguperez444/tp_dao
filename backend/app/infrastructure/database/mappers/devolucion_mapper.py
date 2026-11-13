from app.domain.models.devolucion import Devolucion
from app.infrastructure.database.models.devolucion_orm import DevolucionORM


class DevolucionMapper:
    @staticmethod
    def orm_to_domain(instance: DevolucionORM) -> Devolucion:
        return Devolucion(
            id=instance.id,
            venta_id=instance.venta_id,
            motivo_id=instance.motivo_id,
            metodo_reintegro_id=instance.metodo_reintegro_id,
            detalle=instance.detalle,
            fecha=instance.fecha,
        )

    @staticmethod
    def domain_to_orm(entity: Devolucion) -> DevolucionORM:
        orm = DevolucionORM(
            venta_id=entity.venta_id,
            motivo_id=entity.motivo_id,
            metodo_reintegro_id=entity.metodo_reintegro_id,
            detalle=entity.detalle,
            fecha=entity.fecha,
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
