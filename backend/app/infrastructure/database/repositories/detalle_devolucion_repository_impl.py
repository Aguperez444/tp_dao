from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.application.ports.i_detalle_devolucion_repository import (
    IDetalleDevolucionRepository,
)
from app.domain.models.detalle_devolucion import DetalleDevolucion
from app.infrastructure.database.mappers.detalle_devolucion_mapper import (
    DetalleDevolucionMapper,
)
from app.infrastructure.database.models.detalle_devolucion_orm import (
    DetalleDevolucionORM,
)
from app.infrastructure.database.models.devolucion_orm import DevolucionORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class DetalleDevolucionRepositoryImpl(
    SqlAlchemyEntityRepository[DetalleDevolucion, DetalleDevolucionORM],
    IDetalleDevolucionRepository,
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetalleDevolucionORM)

    def _to_domain(self, instance: DetalleDevolucionORM) -> DetalleDevolucion:
        return DetalleDevolucionMapper.orm_to_domain(instance)

    def _to_orm(self, entity: DetalleDevolucion) -> DetalleDevolucionORM:
        return DetalleDevolucionMapper.domain_to_orm(entity)

    def returned(self, sale_id: int, product_id: int) -> int:
        return self.session.scalar(
            select(func.coalesce(func.sum(DetalleDevolucionORM.cantidad), 0))
            .join(DevolucionORM, DevolucionORM.id == DetalleDevolucionORM.devolucion_id)
            .where(
                DevolucionORM.venta_id == sale_id,
                DetalleDevolucionORM.producto_id == product_id,
            )
        )
