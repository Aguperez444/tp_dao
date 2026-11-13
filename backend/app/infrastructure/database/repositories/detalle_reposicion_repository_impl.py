from sqlalchemy.orm import Session

from app.domain.models.detalle_reposicion import DetalleReposicion
from app.infrastructure.database.mappers.detalle_reposicion_mapper import (
    DetalleReposicionMapper,
)
from app.infrastructure.database.models.detalle_reposicion_orm import (
    DetalleReposicionORM,
)
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class DetalleReposicionRepositoryImpl(
    SqlAlchemyEntityRepository[DetalleReposicion, DetalleReposicionORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetalleReposicionORM)

    def _to_domain(self, instance: DetalleReposicionORM) -> DetalleReposicion:
        return DetalleReposicionMapper.orm_to_domain(instance)

    def _to_orm(self, entity: DetalleReposicion) -> DetalleReposicionORM:
        return DetalleReposicionMapper.domain_to_orm(entity)
