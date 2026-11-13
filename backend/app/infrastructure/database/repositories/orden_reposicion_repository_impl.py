from sqlalchemy.orm import Session

from app.domain.models.orden_reposicion import OrdenReposicion
from app.infrastructure.database.mappers.orden_reposicion_mapper import (
    OrdenReposicionMapper,
)
from app.infrastructure.database.models.orden_reposicion_orm import OrdenReposicionORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class OrdenReposicionRepositoryImpl(
    SqlAlchemyEntityRepository[OrdenReposicion, OrdenReposicionORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, OrdenReposicionORM)

    def _to_domain(self, instance: OrdenReposicionORM) -> OrdenReposicion:
        return OrdenReposicionMapper.orm_to_domain(instance)

    def _to_orm(self, entity: OrdenReposicion) -> OrdenReposicionORM:
        return OrdenReposicionMapper.domain_to_orm(entity)
