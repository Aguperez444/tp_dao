from pathlib import Path
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from .models import Base, EstadoCompra, EstadoReposicion, EstadoRemito, EstadoPrecinto, EstadoBulto, MetodoPago, Motivo
from .repository import SqlAlchemyRepository

LOOKUPS = {
    EstadoCompra: ('Pendiente', 'Recibida'),
    EstadoReposicion: ('Pendiente', 'En preparación', 'En tránsito', 'Completada', 'Con rechazos'),
    EstadoRemito: ('Pendiente', 'En tránsito', 'Recibido', 'Verificado', 'Rechazado'),
    EstadoPrecinto: ('Sin colocar', 'Intacto', 'Violado', 'No coincide'),
    EstadoBulto: ('Preparado', 'Precintado', 'En tránsito', 'Recibido', 'Verificado', 'Rechazado'),
    MetodoPago: ('Efectivo', 'Tarjeta', 'Transferencia'),
    Motivo: ('Cambio solicitado', 'Error en la compra', 'Disconformidad'),
}


class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine('sqlite:///' + str(self.path), connect_args={'check_same_thread': False, 'timeout': 20})
        @event.listens_for(self.engine, 'connect')
        def configure(connection, _):
            connection.isolation_level = None
            connection.execute('PRAGMA foreign_keys=ON')
            connection.execute('PRAGMA busy_timeout=20000')
        self.sessions = sessionmaker(self.engine, expire_on_commit=False)

    def initialize(self):
        # No reutilizar silenciosamente una base de la versión anterior.
        with self.engine.connect() as cx:
            tables = {r[0] for r in cx.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))}
            if tables and not tables.issubset(set(Base.metadata.tables)):
                raise RuntimeError('La base usa un esquema anterior o desconocido. Elija otra ruta NEXO_DB_PATH.')
        Base.metadata.create_all(self.engine)
        with self.uow(write=True) as uow:
            for model, names in LOOKUPS.items():
                for name in names:
                    if not uow.repo.list(model.__tablename__, nombre=name):
                        uow.repo.create(model.__tablename__, {'nombre': name})
        with self.engine.begin() as cx:
            for operation in ('UPDATE', 'DELETE'):
                cx.exec_driver_sql(f'''CREATE TRIGGER IF NOT EXISTS historial_no_{operation.lower()}
                  BEFORE {operation} ON cambio_estado_bulto BEGIN SELECT RAISE(ABORT, 'Historial inmutable'); END''')

    def uow(self, write=False):
        return SqlAlchemyUnitOfWork(self.sessions, write)

    def dispose(self):
        self.engine.dispose()


class SqlAlchemyUnitOfWork:
    def __init__(self, sessions, write):
        self.sessions, self.write = sessions, write

    def __enter__(self):
        self.session = self.sessions()
        try:
            self.session.connection().exec_driver_sql('BEGIN IMMEDIATE' if self.write else 'BEGIN')
            self.repo = SqlAlchemyRepository(self.session)
            return self
        except Exception:
            self.session.close()
            raise

    def __exit__(self, exc_type, exc, traceback):
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
