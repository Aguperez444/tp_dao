from app.domain.models.ciudad import Ciudad
from app.infrastructure.database.models.ciudad_orm import CiudadORM


class CiudadMapper:
    @staticmethod
    def orm_to_domain(instance: CiudadORM) -> Ciudad:
        return Ciudad(
            id=instance.id, nombre=instance.nombre, provincia_id=instance.provincia_id
        )

    @staticmethod
    def domain_to_orm(entity: Ciudad) -> CiudadORM:
        orm = CiudadORM(
            nombre=entity.nombre,
            provincia_id=entity.provincia_id,
        )
        if entity.id is not None:
            orm.id = entity.id
        return orm
