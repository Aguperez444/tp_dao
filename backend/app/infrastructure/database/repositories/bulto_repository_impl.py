from sqlalchemy.orm import Session

from app.domain.models.bulto import Bulto
from app.infrastructure.database.mappers.bulto_mapper import BultoMapper
from app.infrastructure.database.models.bulto_orm import BultoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class BultoRepositoryImpl(SqlAlchemyEntityRepository[Bulto, BultoORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, BultoORM)

    def _to_domain(self, instance: BultoORM) -> Bulto:
        return BultoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Bulto) -> BultoORM:
        return BultoMapper.domain_to_orm(entity)
