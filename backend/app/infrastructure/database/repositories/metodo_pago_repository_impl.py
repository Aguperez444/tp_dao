from sqlalchemy.orm import Session

from app.domain.models.metodo_pago import MetodoPago
from app.infrastructure.database.mappers.metodo_pago_mapper import MetodoPagoMapper
from app.infrastructure.database.models.metodo_pago_orm import MetodoPagoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class MetodoPagoRepositoryImpl(SqlAlchemyEntityRepository[MetodoPago, MetodoPagoORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, MetodoPagoORM)

    def _to_domain(self, instance: MetodoPagoORM) -> MetodoPago:
        return MetodoPagoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: MetodoPago) -> MetodoPagoORM:
        return MetodoPagoMapper.domain_to_orm(entity)
