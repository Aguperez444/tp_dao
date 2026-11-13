from app.infrastructure.database.base import Base
from app.infrastructure.database.models.named import Named


class EstadoCompraORM(Named, Base):
    __tablename__ = "estado_compra"
