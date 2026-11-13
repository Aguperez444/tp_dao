from app.domain.models.provincia import Provincia
from app.infrastructure.database.models.provincia_orm import ProvinciaORM


class ProvinciaMapper:
    @staticmethod
    def orm_to_domain(instance: ProvinciaORM) -> Provincia:
        return Provincia(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: Provincia) -> ProvinciaORM:
        orm = ProvinciaORM(
            nombre=entity.nombre
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm