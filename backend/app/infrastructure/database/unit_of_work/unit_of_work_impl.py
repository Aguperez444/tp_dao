from types import TracebackType

from sqlalchemy.orm import Session, sessionmaker

from app.application.ports.i_unit_of_work import IUnitOfWork
from app.infrastructure.database.repositories.bulto_repository_impl import (
    BultoRepositoryImpl,
)
from app.infrastructure.database.repositories.cambio_estado_bulto_repository_impl import (
    CambioEstadoBultoRepositoryImpl,
)
from app.infrastructure.database.repositories.categoria_repository_impl import (
    CategoriaRepositoryImpl,
)
from app.infrastructure.database.repositories.ciudad_repository_impl import (
    CiudadRepositoryImpl,
)
from app.infrastructure.database.repositories.compra_repository_impl import (
    CompraRepositoryImpl,
)
from app.infrastructure.database.repositories.detalle_bulto_repository_impl import (
    DetalleBultoRepositoryImpl,
)
from app.infrastructure.database.repositories.detalle_compra_repository_impl import (
    DetalleCompraRepositoryImpl,
)
from app.infrastructure.database.repositories.detalle_devolucion_repository_impl import (
    DetalleDevolucionRepositoryImpl,
)
from app.infrastructure.database.repositories.detalle_reposicion_repository_impl import (
    DetalleReposicionRepositoryImpl,
)
from app.infrastructure.database.repositories.detalle_venta_repository_impl import (
    DetalleVentaRepositoryImpl,
)
from app.infrastructure.database.repositories.devolucion_repository_impl import (
    DevolucionRepositoryImpl,
)
from app.infrastructure.database.repositories.domicilio_repository_impl import (
    DomicilioRepositoryImpl,
)
from app.infrastructure.database.repositories.establecimiento_repository_impl import (
    EstablecimientoRepositoryImpl,
)
from app.infrastructure.database.repositories.estado_bulto_repository_impl import (
    EstadoBultoRepositoryImpl,
)
from app.infrastructure.database.repositories.estado_compra_repository_impl import (
    EstadoCompraRepositoryImpl,
)
from app.infrastructure.database.repositories.estado_precinto_repository_impl import (
    EstadoPrecintoRepositoryImpl,
)
from app.infrastructure.database.repositories.estado_remito_repository_impl import (
    EstadoRemitoRepositoryImpl,
)
from app.infrastructure.database.repositories.estado_reposicion_repository_impl import (
    EstadoReposicionRepositoryImpl,
)
from app.infrastructure.database.repositories.existencia_repository_impl import (
    ExistenciaRepositoryImpl,
)
from app.infrastructure.database.repositories.metodo_pago_repository_impl import (
    MetodoPagoRepositoryImpl,
)
from app.infrastructure.database.repositories.motivo_repository_impl import (
    MotivoRepositoryImpl,
)
from app.infrastructure.database.repositories.orden_reposicion_repository_impl import (
    OrdenReposicionRepositoryImpl,
)
from app.infrastructure.database.repositories.producto_repository_impl import (
    ProductoRepositoryImpl,
)
from app.infrastructure.database.repositories.proveedor_repository_impl import (
    ProveedorRepositoryImpl,
)
from app.infrastructure.database.repositories.provincia_repository_impl import (
    ProvinciaRepositoryImpl,
)
from app.infrastructure.database.repositories.remito_repository_impl import (
    RemitoRepositoryImpl,
)
from app.infrastructure.database.repositories.venta_repository_impl import (
    VentaRepositoryImpl,
)


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, sessions: sessionmaker[Session], write: bool) -> None:
        self.sessions = sessions
        self.write = write

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self.sessions()
        try:
            self.session.connection().exec_driver_sql(
                "BEGIN IMMEDIATE" if self.write else "BEGIN"
            )
            self.categoria_repo = CategoriaRepositoryImpl(self.session)
            self.provincia_repo = ProvinciaRepositoryImpl(self.session)
            self.ciudad_repo = CiudadRepositoryImpl(self.session)
            self.domicilio_repo = DomicilioRepositoryImpl(self.session)
            self.establecimiento_repo = EstablecimientoRepositoryImpl(self.session)
            self.proveedor_repo = ProveedorRepositoryImpl(self.session)
            self.producto_repo = ProductoRepositoryImpl(self.session)
            self.existencia_repo = ExistenciaRepositoryImpl(self.session)
            self.estado_compra_repo = EstadoCompraRepositoryImpl(self.session)
            self.compra_repo = CompraRepositoryImpl(self.session)
            self.detalle_compra_repo = DetalleCompraRepositoryImpl(self.session)
            self.estado_reposicion_repo = EstadoReposicionRepositoryImpl(self.session)
            self.orden_reposicion_repo = OrdenReposicionRepositoryImpl(self.session)
            self.detalle_reposicion_repo = DetalleReposicionRepositoryImpl(self.session)
            self.estado_remito_repo = EstadoRemitoRepositoryImpl(self.session)
            self.remito_repo = RemitoRepositoryImpl(self.session)
            self.estado_precinto_repo = EstadoPrecintoRepositoryImpl(self.session)
            self.estado_bulto_repo = EstadoBultoRepositoryImpl(self.session)
            self.bulto_repo = BultoRepositoryImpl(self.session)
            self.detalle_bulto_repo = DetalleBultoRepositoryImpl(self.session)
            self.cambio_estado_bulto_repo = CambioEstadoBultoRepositoryImpl(
                self.session
            )
            self.metodo_pago_repo = MetodoPagoRepositoryImpl(self.session)
            self.venta_repo = VentaRepositoryImpl(self.session)
            self.detalle_venta_repo = DetalleVentaRepositoryImpl(self.session)
            self.motivo_repo = MotivoRepositoryImpl(self.session)
            self.devolucion_repo = DevolucionRepositoryImpl(self.session)
            self.detalle_devolucion_repo = DetalleDevolucionRepositoryImpl(self.session)
            return self
        except Exception:
            self.session.close()
            raise

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
