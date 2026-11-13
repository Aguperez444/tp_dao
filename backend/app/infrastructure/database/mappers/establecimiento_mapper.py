from app.domain.models.establecimiento import Establecimiento
from app.infrastructure.database.models.establecimiento_orm import EstablecimientoORM


class EstablecimientoMapper:
    @staticmethod
    def orm_to_domain(instance: EstablecimientoORM) -> Establecimiento:
        return Establecimiento(
            id=instance.id,
            nombre=instance.nombre,
            es_central=instance.es_central,
            domicilio_id=instance.domicilio_id,
        )

    @staticmethod
    def domain_to_orm(entity: Establecimiento) -> EstablecimientoORM:
        orm = EstablecimientoORM(
            nombre=entity.nombre,
            es_central=entity.es_central,
            domicilio_id=entity.domicilio_id,
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
