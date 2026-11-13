from app.infrastructure.database.base import Base
from app.infrastructure.database.models.named import Named


class CategoriaORM(Named, Base):
    __tablename__ = "categoria"
