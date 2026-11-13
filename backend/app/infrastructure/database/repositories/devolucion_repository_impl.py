from sqlalchemy.orm import Session

from app.domain.models.devolucion import Devolucion
from app.infrastructure.database.mappers.devolucion_mapper import DevolucionMapper
from app.infrastructure.database.models.devolucion_orm import DevolucionORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class DevolucionRepositoryImpl(SqlAlchemyEntityRepository[Devolucion, DevolucionORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DevolucionORM)

    def _to_domain(self, instance: DevolucionORM) -> Devolucion:
        return DevolucionMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Devolucion) -> DevolucionORM:
        return DevolucionMapper.domain_to_orm(entity)
