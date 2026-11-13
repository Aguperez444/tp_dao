from sqlalchemy.orm import Session

from app.domain.models.estado_bulto import EstadoBulto
from app.infrastructure.database.mappers.estado_bulto_mapper import EstadoBultoMapper
from app.infrastructure.database.models.estado_bulto_orm import EstadoBultoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class EstadoBultoRepositoryImpl(
    SqlAlchemyEntityRepository[EstadoBulto, EstadoBultoORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, EstadoBultoORM)

    def _to_domain(self, instance: EstadoBultoORM) -> EstadoBulto:
        return EstadoBultoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: EstadoBulto) -> EstadoBultoORM:
        return EstadoBultoMapper.domain_to_orm(entity)
