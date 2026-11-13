from sqlalchemy.orm import Session

from app.domain.models.detalle_bulto import DetalleBulto
from app.infrastructure.database.mappers.detalle_bulto_mapper import DetalleBultoMapper
from app.infrastructure.database.models.detalle_bulto_orm import DetalleBultoORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class DetalleBultoRepositoryImpl(
    SqlAlchemyEntityRepository[DetalleBulto, DetalleBultoORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, DetalleBultoORM)

    def _to_domain(self, instance: DetalleBultoORM) -> DetalleBulto:
        return DetalleBultoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: DetalleBulto) -> DetalleBultoORM:
        return DetalleBultoMapper.domain_to_orm(entity)
