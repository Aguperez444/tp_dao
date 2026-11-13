from sqlalchemy.orm import Session

from app.domain.models.detalle_compra import DetalleCompra
from app.infrastructure.database.mappers.detalle_compra_mapper import (
    DetalleCompraMapper,
)
from app.infrastructure.database.models.detalle_compra_orm import DetalleCompraORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class DetalleCompraRepositoryImpl(
    SqlAlchemyEntityRepository[DetalleCompra, DetalleCompraORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetalleCompraORM)

    def _to_domain(self, instance: DetalleCompraORM) -> DetalleCompra:
        return DetalleCompraMapper.orm_to_domain(instance)

    def _to_orm(self, entity: DetalleCompra) -> DetalleCompraORM:
        return DetalleCompraMapper.domain_to_orm(entity)
