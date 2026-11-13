from abc import abstractmethod

from app.application.ports.i_entity_repository import IEntityRepository
from app.domain.models.detalle_devolucion import DetalleDevolucion


class IDetalleDevolucionRepository(IEntityRepository[DetalleDevolucion]):
    @abstractmethod
    def returned(self, sale_id: int, product_id: int) -> int:
        raise NotImplementedError
