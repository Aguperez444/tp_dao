from app.infrastructure.database.base import Base
from app.infrastructure.database.models.named import Named


class EstadoBultoORM(Named, Base):
    __tablename__ = "estado_bulto"
