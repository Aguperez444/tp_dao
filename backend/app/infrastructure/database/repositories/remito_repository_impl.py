from sqlalchemy.orm import Session

from app.domain.models.remito import Remito
from app.infrastructure.database.mappers.remito_mapper import RemitoMapper
from app.infrastructure.database.models.remito_orm import RemitoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class RemitoRepositoryImpl(SqlAlchemyEntityRepository[Remito, RemitoORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, RemitoORM)

    def _to_domain(self, instance: RemitoORM) -> Remito:
        return RemitoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Remito) -> RemitoORM:
        return RemitoMapper.domain_to_orm(entity)
