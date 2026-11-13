from sqlalchemy.orm import Session

from app.domain.models.estado_remito import EstadoRemito
from app.infrastructure.database.mappers.estado_remito_mapper import EstadoRemitoMapper
from app.infrastructure.database.models.estado_remito_orm import EstadoRemitoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class EstadoRemitoRepositoryImpl(
    SqlAlchemyEntityRepository[EstadoRemito, EstadoRemitoORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, EstadoRemitoORM)

    def _to_domain(self, instance: EstadoRemitoORM) -> EstadoRemito:
        return EstadoRemitoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: EstadoRemito) -> EstadoRemitoORM:
        return EstadoRemitoMapper.domain_to_orm(entity)
