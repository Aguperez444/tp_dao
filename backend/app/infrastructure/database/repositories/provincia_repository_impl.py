from sqlalchemy.orm import Session

from app.domain.models.provincia import Provincia
from app.infrastructure.database.mappers.provincia_mapper import ProvinciaMapper
from app.infrastructure.database.models.provincia_orm import ProvinciaORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class ProvinciaRepositoryImpl(SqlAlchemyEntityRepository[Provincia, ProvinciaORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ProvinciaORM)

    def _to_domain(self, instance: ProvinciaORM) -> Provincia:
        return ProvinciaMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Provincia) -> ProvinciaORM:
        return ProvinciaMapper.domain_to_orm(entity)
