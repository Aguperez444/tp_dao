from sqlalchemy.orm import Session

from app.domain.models.domicilio import Domicilio
from app.infrastructure.database.mappers.domicilio_mapper import DomicilioMapper
from app.infrastructure.database.models.domicilio_orm import DomicilioORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class DomicilioRepositoryImpl(SqlAlchemyEntityRepository[Domicilio, DomicilioORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DomicilioORM)

    def _to_domain(self, instance: DomicilioORM) -> Domicilio:
        return DomicilioMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Domicilio) -> DomicilioORM:
        return DomicilioMapper.domain_to_orm(entity)
