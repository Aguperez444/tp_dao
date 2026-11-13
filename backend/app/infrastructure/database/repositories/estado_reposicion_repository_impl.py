from sqlalchemy.orm import Session

from app.domain.models.estado_reposicion import EstadoReposicion
from app.infrastructure.database.mappers.estado_reposicion_mapper import (
    EstadoReposicionMapper,
)
from app.infrastructure.database.models.estado_reposicion_orm import EstadoReposicionORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class EstadoReposicionRepositoryImpl(
    SqlAlchemyEntityRepository[EstadoReposicion, EstadoReposicionORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, EstadoReposicionORM)

    def _to_domain(self, instance: EstadoReposicionORM) -> EstadoReposicion:
        return EstadoReposicionMapper.orm_to_domain(instance)

    def _to_orm(self, entity: EstadoReposicion) -> EstadoReposicionORM:
        return EstadoReposicionMapper.domain_to_orm(entity)
