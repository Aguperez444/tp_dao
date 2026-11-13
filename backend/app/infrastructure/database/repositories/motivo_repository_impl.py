from sqlalchemy.orm import Session

from app.domain.models.motivo import Motivo
from app.infrastructure.database.mappers.motivo_mapper import MotivoMapper
from app.infrastructure.database.models.motivo_orm import MotivoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class MotivoRepositoryImpl(SqlAlchemyEntityRepository[Motivo, MotivoORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, MotivoORM)

    def _to_domain(self, instance: MotivoORM) -> Motivo:
        return MotivoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Motivo) -> MotivoORM:
        return MotivoMapper.domain_to_orm(entity)
