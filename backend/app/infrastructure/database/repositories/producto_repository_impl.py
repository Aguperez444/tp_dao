from sqlalchemy.orm import Session

from app.domain.models.producto import Producto
from app.infrastructure.database.mappers.producto_mapper import ProductoMapper
from app.infrastructure.database.models.producto_orm import ProductoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class ProductoRepositoryImpl(SqlAlchemyEntityRepository[Producto, ProductoORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ProductoORM)

    def _to_domain(self, instance: ProductoORM) -> Producto:
        return ProductoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Producto) -> ProductoORM:
        return ProductoMapper.domain_to_orm(entity)
