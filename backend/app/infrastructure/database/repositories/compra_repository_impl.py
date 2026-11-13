from sqlalchemy.orm import Session

from app.domain.models.compra import Compra
from app.infrastructure.database.mappers.compra_mapper import CompraMapper
from app.infrastructure.database.models.compra_orm import CompraORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class CompraRepositoryImpl(SqlAlchemyEntityRepository[Compra, CompraORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, CompraORM)

    def _to_domain(self, instance: CompraORM) -> Compra:
        return CompraMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Compra) -> CompraORM:
        return CompraMapper.domain_to_orm(entity)
