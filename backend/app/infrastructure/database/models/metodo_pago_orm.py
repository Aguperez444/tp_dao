from app.infrastructure.database.base import Base
from app.infrastructure.database.models.named import Named


class MetodoPagoORM(Named, Base):
    __tablename__ = "metodo_pago"
