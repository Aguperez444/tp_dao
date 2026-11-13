from sqlalchemy.orm import Session

from app.domain.models.categoria import Categoria
from app.infrastructure.database.mappers.categoria_mapper import CategoriaMapper
from app.infrastructure.database.models.categoria_orm import CategoriaORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class CategoriaRepositoryImpl(SqlAlchemyEntityRepository[Categoria, CategoriaORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, CategoriaORM)

    def _to_domain(self, instance: CategoriaORM) -> Categoria:
        return CategoriaMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Categoria) -> CategoriaORM:
        return CategoriaMapper.domain_to_orm(entity)
