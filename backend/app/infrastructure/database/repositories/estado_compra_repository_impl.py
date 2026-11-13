from sqlalchemy.orm import Session

from app.domain.models.estado_compra import EstadoCompra
from app.infrastructure.database.mappers.estado_compra_mapper import EstadoCompraMapper
from app.infrastructure.database.models.estado_compra_orm import EstadoCompraORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class EstadoCompraRepositoryImpl(
    SqlAlchemyEntityRepository[EstadoCompra, EstadoCompraORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, EstadoCompraORM)

    def _to_domain(self, instance: EstadoCompraORM) -> EstadoCompra:
        return EstadoCompraMapper.orm_to_domain(instance)

    def _to_orm(self, entity: EstadoCompra) -> EstadoCompraORM:
        return EstadoCompraMapper.domain_to_orm(entity)
