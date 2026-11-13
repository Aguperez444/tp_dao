from pathlib import Path
from sqlite3 import Connection

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import ConnectionPoolEntry

from app.domain.models.estado_bulto import EstadoBulto
from app.domain.models.estado_compra import EstadoCompra
from app.domain.models.estado_precinto import EstadoPrecinto
from app.domain.models.estado_remito import EstadoRemito
from app.domain.models.estado_reposicion import EstadoReposicion
from app.domain.models.metodo_pago import MetodoPago
from app.domain.models.motivo import Motivo
from app.infrastructure.database.base import Base
from app.infrastructure.database.lookup_data import LOOKUPS
from app.infrastructure.database.models.estado_bulto_orm import EstadoBultoORM
from app.infrastructure.database.models.estado_compra_orm import EstadoCompraORM
from app.infrastructure.database.models.estado_precinto_orm import EstadoPrecintoORM
from app.infrastructure.database.models.estado_remito_orm import EstadoRemitoORM
from app.infrastructure.database.models.estado_reposicion_orm import EstadoReposicionORM
from app.infrastructure.database.models.metodo_pago_orm import MetodoPagoORM
from app.infrastructure.database.models.motivo_orm import MotivoORM
from app.infrastructure.database.unit_of_work.unit_of_work_impl import (
    SqlAlchemyUnitOfWork,
)
from app.infrastructure.database.unit_of_work.uow_factory import uow_factory


class Database:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(
            "sqlite:///" + str(self.path),
            connect_args={"check_same_thread": False, "timeout": 20},
        )

        @event.listens_for(self.engine, "connect")
        def configure(connection: Connection, _: ConnectionPoolEntry) -> None:
            connection.isolation_level = None
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("PRAGMA busy_timeout=20000")

        self.sessions = sessionmaker(self.engine, expire_on_commit=False)

    def initialize(self) -> None:
        # No reutilizar silenciosamente una base de la versión anterior.
        with self.engine.connect() as cx:
            tables = {
                r[0]
                for r in cx.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table'")
                )
            }
            if tables and not tables.issubset(set(Base.metadata.tables)):
                raise RuntimeError(
                    "La base usa un esquema anterior o desconocido. Elija otra ruta NEXO_DB_PATH."
                )
        Base.metadata.create_all(self.engine)
        with self.uow(write=True) as uow:
            for name in LOOKUPS[EstadoCompraORM]:
                if not uow.estado_compra_repo.list(nombre=name):
                    uow.estado_compra_repo.save(EstadoCompra(nombre=name))
            for name in LOOKUPS[EstadoReposicionORM]:
                if not uow.estado_reposicion_repo.list(nombre=name):
                    uow.estado_reposicion_repo.save(EstadoReposicion(nombre=name))
            for name in LOOKUPS[EstadoRemitoORM]:
                if not uow.estado_remito_repo.list(nombre=name):
                    uow.estado_remito_repo.save(EstadoRemito(nombre=name))
            for name in LOOKUPS[EstadoPrecintoORM]:
                if not uow.estado_precinto_repo.list(nombre=name):
                    uow.estado_precinto_repo.save(EstadoPrecinto(nombre=name))
            for name in LOOKUPS[EstadoBultoORM]:
                if not uow.estado_bulto_repo.list(nombre=name):
                    uow.estado_bulto_repo.save(EstadoBulto(nombre=name))
            for name in LOOKUPS[MetodoPagoORM]:
                if not uow.metodo_pago_repo.list(nombre=name):
                    uow.metodo_pago_repo.save(MetodoPago(nombre=name))
            for name in LOOKUPS[MotivoORM]:
                if not uow.motivo_repo.list(nombre=name):
                    uow.motivo_repo.save(Motivo(nombre=name))
        with self.engine.begin() as cx:
            for operation in ("UPDATE", "DELETE"):
                cx.exec_driver_sql(f"""CREATE TRIGGER IF NOT EXISTS historial_no_{operation.lower()}
                  BEFORE {operation} ON cambio_estado_bulto BEGIN SELECT RAISE(ABORT, 'Historial inmutable'); END""")

    def uow(self, write: bool = False) -> SqlAlchemyUnitOfWork:
        return uow_factory(self.sessions, write)

    def dispose(self) -> None:
        self.engine.dispose()
