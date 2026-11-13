from sqlalchemy.orm import Session

from app.domain.models.venta import Venta
from app.infrastructure.database.mappers.venta_mapper import VentaMapper
from app.infrastructure.database.models.venta_orm import VentaORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class VentaRepositoryImpl(SqlAlchemyEntityRepository[Venta, VentaORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, VentaORM)

    def _to_domain(self, instance: VentaORM) -> Venta:
        return VentaMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Venta) -> VentaORM:
        return VentaMapper.domain_to_orm(entity)
