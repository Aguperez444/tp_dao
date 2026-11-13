from sqlalchemy.orm import Session

from app.domain.models.estado_precinto import EstadoPrecinto
from app.infrastructure.database.mappers.estado_precinto_mapper import (
    EstadoPrecintoMapper,
)
from app.infrastructure.database.models.estado_precinto_orm import EstadoPrecintoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class EstadoPrecintoRepositoryImpl(
    SqlAlchemyEntityRepository[EstadoPrecinto, EstadoPrecintoORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, EstadoPrecintoORM)

    def _to_domain(self, instance: EstadoPrecintoORM) -> EstadoPrecinto:
        return EstadoPrecintoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: EstadoPrecinto) -> EstadoPrecintoORM:
        return EstadoPrecintoMapper.domain_to_orm(entity)
