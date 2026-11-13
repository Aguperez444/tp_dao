from abc import abstractmethod

from app.application.ports.i_entity_repository import IEntityRepository
from app.domain.models.existencia import Existencia


class IExistenciaRepository(IEntityRepository[Existencia]):
    @abstractmethod
    def stock(self, establishment_id: int, product_id: int) -> Existencia:
        raise NotImplementedError
