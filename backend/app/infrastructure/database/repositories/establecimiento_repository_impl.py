from sqlalchemy.orm import Session

from app.domain.models.establecimiento import Establecimiento
from app.infrastructure.database.mappers.establecimiento_mapper import (
    EstablecimientoMapper,
)
from app.infrastructure.database.models.establecimiento_orm import EstablecimientoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class EstablecimientoRepositoryImpl(
    SqlAlchemyEntityRepository[Establecimiento, EstablecimientoORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, EstablecimientoORM)

    def _to_domain(self, instance: EstablecimientoORM) -> Establecimiento:
        return EstablecimientoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Establecimiento) -> EstablecimientoORM:
        return EstablecimientoMapper.domain_to_orm(entity)
