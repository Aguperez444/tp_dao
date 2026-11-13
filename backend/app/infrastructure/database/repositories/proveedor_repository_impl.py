from sqlalchemy.orm import Session

from app.domain.models.proveedor import Proveedor
from app.infrastructure.database.mappers.proveedor_mapper import ProveedorMapper
from app.infrastructure.database.models.proveedor_orm import ProveedorORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class ProveedorRepositoryImpl(SqlAlchemyEntityRepository[Proveedor, ProveedorORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ProveedorORM)

    def _to_domain(self, instance: ProveedorORM) -> Proveedor:
        return ProveedorMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Proveedor) -> ProveedorORM:
        return ProveedorMapper.domain_to_orm(entity)
