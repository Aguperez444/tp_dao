from abc import ABC, abstractmethod
from types import TracebackType

from app.application.ports.i_detalle_devolucion_repository import (
    IDetalleDevolucionRepository,
)
from app.application.ports.i_entity_repository import IEntityRepository
from app.application.ports.i_existencia_repository import IExistenciaRepository
from app.domain.models.bulto import Bulto
from app.domain.models.cambio_estado_bulto import CambioEstadoBulto
from app.domain.models.categoria import Categoria
from app.domain.models.ciudad import Ciudad
from app.domain.models.compra import Compra
from app.domain.models.detalle_bulto import DetalleBulto
from app.domain.models.detalle_compra import DetalleCompra
from app.domain.models.detalle_reposicion import DetalleReposicion
from app.domain.models.detalle_venta import DetalleVenta
from app.domain.models.devolucion import Devolucion
from app.domain.models.domicilio import Domicilio
from app.domain.models.establecimiento import Establecimiento
from app.domain.models.estado_bulto import EstadoBulto
from app.domain.models.estado_compra import EstadoCompra
from app.domain.models.estado_precinto import EstadoPrecinto
from app.domain.models.estado_remito import EstadoRemito
from app.domain.models.estado_reposicion import EstadoReposicion
from app.domain.models.metodo_pago import MetodoPago
from app.domain.models.motivo import Motivo
from app.domain.models.orden_reposicion import OrdenReposicion
from app.domain.models.producto import Producto
from app.domain.models.proveedor import Proveedor
from app.domain.models.provincia import Provincia
from app.domain.models.remito import Remito
from app.domain.models.venta import Venta


class IUnitOfWork(ABC):
    categoria_repo: IEntityRepository[Categoria]
    provincia_repo: IEntityRepository[Provincia]
    ciudad_repo: IEntityRepository[Ciudad]
    domicilio_repo: IEntityRepository[Domicilio]
    establecimiento_repo: IEntityRepository[Establecimiento]
    proveedor_repo: IEntityRepository[Proveedor]
    producto_repo: IEntityRepository[Producto]
    existencia_repo: IExistenciaRepository
    estado_compra_repo: IEntityRepository[EstadoCompra]
    compra_repo: IEntityRepository[Compra]
    detalle_compra_repo: IEntityRepository[DetalleCompra]
    estado_reposicion_repo: IEntityRepository[EstadoReposicion]
    orden_reposicion_repo: IEntityRepository[OrdenReposicion]
    detalle_reposicion_repo: IEntityRepository[DetalleReposicion]
    estado_remito_repo: IEntityRepository[EstadoRemito]
    remito_repo: IEntityRepository[Remito]
    estado_precinto_repo: IEntityRepository[EstadoPrecinto]
    estado_bulto_repo: IEntityRepository[EstadoBulto]
    bulto_repo: IEntityRepository[Bulto]
    detalle_bulto_repo: IEntityRepository[DetalleBulto]
    cambio_estado_bulto_repo: IEntityRepository[CambioEstadoBulto]
    metodo_pago_repo: IEntityRepository[MetodoPago]
    venta_repo: IEntityRepository[Venta]
    detalle_venta_repo: IEntityRepository[DetalleVenta]
    motivo_repo: IEntityRepository[Motivo]
    devolucion_repo: IEntityRepository[Devolucion]
    detalle_devolucion_repo: IDetalleDevolucionRepository

    @abstractmethod
    def __enter__(self) -> "IUnitOfWork":
        raise NotImplementedError

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
