from app.domain.models.provincia import Provincia
from app.infrastructure.database.models.provincia_orm import ProvinciaORM


class ProvinciaMapper:
    @staticmethod
    def orm_to_domain(instance: ProvinciaORM) -> Provincia:
        return Provincia(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: Provincia) -> ProvinciaORM:
        return ProvinciaORM(
            id=entity.id if entity.is_persisted() else None, nombre=entity.nombre
        )
