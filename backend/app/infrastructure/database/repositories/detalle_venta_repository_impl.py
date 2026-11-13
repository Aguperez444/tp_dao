from sqlalchemy.orm import Session

from app.domain.models.detalle_venta import DetalleVenta
from app.infrastructure.database.mappers.detalle_venta_mapper import DetalleVentaMapper
from app.infrastructure.database.models.detalle_venta_orm import DetalleVentaORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class DetalleVentaRepositoryImpl(
    SqlAlchemyEntityRepository[DetalleVenta, DetalleVentaORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetalleVentaORM)

    def _to_domain(self, instance: DetalleVentaORM) -> DetalleVenta:
        return DetalleVentaMapper.orm_to_domain(instance)

    def _to_orm(self, entity: DetalleVenta) -> DetalleVentaORM:
        return DetalleVentaMapper.domain_to_orm(entity)
