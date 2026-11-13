from sqlalchemy.orm import Session

from app.application.ports.i_existencia_repository import IExistenciaRepository
from app.domain.models.existencia import Existencia
from app.infrastructure.database.mappers.existencia_mapper import ExistenciaMapper
from app.infrastructure.database.models.existencia_orm import ExistenciaORM
from app.infrastructure.database.repositories.sqlalchemy_entity_repository import (
    SqlAlchemyEntityRepository,
)


class ExistenciaRepositoryImpl(
    SqlAlchemyEntityRepository[Existencia, ExistenciaORM], IExistenciaRepository
):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ExistenciaORM)

    def _to_domain(self, instance: ExistenciaORM) -> Existencia:
        return ExistenciaMapper.orm_to_domain(instance)

    def _to_orm(self, entity: Existencia) -> ExistenciaORM:
        return ExistenciaMapper.domain_to_orm(entity)

    def stock(self, establishment_id: int, product_id: int) -> Existencia:
        rows = self.list(establecimiento_id=establishment_id, producto_id=product_id)
        return (
            rows[0]
            if rows
            else self.save(
                Existencia(
                    establecimiento_id=establishment_id,
                    producto_id=product_id,
                    almacenado_total=0,
                    reservado=0,
                    minimo_permitido=0,
                )
            )
        )
