from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ProveedorORM(Base):
    __tablename__ = "proveedor"
    id: Mapped[int] = mapped_column(primary_key=True)
    CUIT: Mapped[str] = mapped_column(String(11), unique=True)
    nombre: Mapped[str] = mapped_column(String(150))
    esta_activo: Mapped[bool] = mapped_column(Boolean, default=True)
