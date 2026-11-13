from abc import abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.ports.i_entity_repository import (
    EntityT,
    FilterValue,
    IEntityRepository,
)
from app.infrastructure.database.base import Base

OrmT = TypeVar("OrmT", bound=Base)


class SqlAlchemyEntityRepository(IEntityRepository[EntityT], Generic[EntityT, OrmT]):
    def __init__(self, session: Session, model: type[OrmT]) -> None:
        self.session = session
        self.model = model
        self.resource_name = model.__table__.name

    @abstractmethod
    def _to_domain(self, instance: OrmT) -> EntityT:
        raise NotImplementedError

    @abstractmethod
    def _to_orm(self, entity: EntityT) -> OrmT:
        raise NotImplementedError

    def get(self, entity_id: int) -> EntityT | None:
        instance = self.session.get(self.model, entity_id)
        return self._to_domain(instance) if instance is not None else None

    def list(self, **filters: FilterValue) -> list[EntityT]:
        statement = (
            select(self.model).filter_by(**filters).order_by(self.model.__table__.c.id)
        )
        return [self._to_domain(row) for row in self.session.scalars(statement)]

    def save(self, entity: EntityT) -> EntityT:
        instance = self._to_orm(entity)
        self.session.add(instance)
        self.session.flush()
        return self._to_domain(instance)

    def update(self, entity: EntityT) -> EntityT:
        instance = self.session.get(self.model, entity.id)
        assert instance is not None
        mapped = self._to_orm(entity)
        for column in self.model.__table__.columns:
            if column.name != "id":
                setattr(instance, column.name, getattr(mapped, column.name))
        self.session.flush()
        return self._to_domain(instance)
