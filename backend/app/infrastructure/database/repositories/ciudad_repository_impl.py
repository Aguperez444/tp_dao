from sqlalchemy.orm import Session

from app.domain.models.ciudad import Ciudad
from app.infrastructure.database.mappers.ciudad_mapper import CiudadMapper
from app.infrastructure.database.models.ciudad_orm import CiudadORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class CiudadRepositoryImpl(SqlAlchemyEntityRepository[Ciudad, CiudadORM]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, CiudadORM)

    def _to_domain(self, instance: CiudadORM) -> Ciudad:
        return CiudadMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Ciudad) -> CiudadORM:
        return CiudadMapper.domain_to_orm(entity)
