from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ProductoORM(Base):
    __tablename__ = "producto"
    __table_args__ = (CheckConstraint("precio > 0 AND costo_referencia >= 0"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    detalle: Mapped[str] = mapped_column(Text, default="")
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"))
    precio: Mapped[int] = mapped_column(Integer)
    costo_referencia: Mapped[int] = mapped_column(Integer)
    esta_activo: Mapped[bool] = mapped_column(Boolean, default=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True)
