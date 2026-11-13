from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.domain.models.entity import Entity

EntityT = TypeVar("EntityT", bound=Entity)
FilterValue = str | int | bool | None


class IEntityRepository(ABC, Generic[EntityT]):
    resource_name: str

    @abstractmethod
    def get(self, entity_id: int) -> EntityT | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, **filters: FilterValue) -> list[EntityT]:
        raise NotImplementedError

    @abstractmethod
    def save(self, entity: EntityT) -> EntityT:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: EntityT) -> EntityT:
        raise NotImplementedError
