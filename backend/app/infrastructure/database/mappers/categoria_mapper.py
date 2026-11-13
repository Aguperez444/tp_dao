from app.domain.models.categoria import Categoria
from app.infrastructure.database.models.categoria_orm import CategoriaORM


class CategoriaMapper:
    @staticmethod
    def orm_to_domain(instance: CategoriaORM) -> Categoria:
        return Categoria(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: Categoria) -> CategoriaORM:
        orm = CategoriaORM(
            nombre=entity.nombre
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
