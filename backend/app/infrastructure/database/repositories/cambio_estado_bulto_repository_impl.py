from sqlalchemy.orm import Session

from app.domain.models.cambio_estado_bulto import CambioEstadoBulto
from app.infrastructure.database.mappers.cambio_estado_bulto_mapper import (
    CambioEstadoBultoMapper,
)
from app.infrastructure.database.models.cambio_estado_bulto_orm import (
    CambioEstadoBultoORM,
)
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class CambioEstadoBultoRepositoryImpl(
    SqlAlchemyEntityRepository[CambioEstadoBulto, CambioEstadoBultoORM]
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, CambioEstadoBultoORM)

    def _to_domain(self, instance: CambioEstadoBultoORM) -> CambioEstadoBulto:
        return CambioEstadoBultoMapper.orm_to_domain(instance)

    def _to_orm(self, entity: CambioEstadoBulto) -> CambioEstadoBultoORM:
        return CambioEstadoBultoMapper.domain_to_orm(entity)
