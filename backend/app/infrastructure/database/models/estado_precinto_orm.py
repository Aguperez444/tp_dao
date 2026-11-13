from app.infrastructure.database.base import Base
from app.infrastructure.database.models.named import Named


class EstadoPrecintoORM(Named, Base):
    __tablename__ = "estado_precinto"
