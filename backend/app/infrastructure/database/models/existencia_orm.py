from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ExistenciaORM(Base):
    __tablename__ = "existencia"
    __table_args__ = (
        UniqueConstraint("establecimiento_id", "producto_id"),
        CheckConstraint(
            "almacenado_total >= reservado AND reservado >= 0 AND minimo_permitido >= 0"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    establecimiento_id: Mapped[int] = mapped_column(ForeignKey("establecimiento.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"))
    almacenado_total: Mapped[int] = mapped_column(Integer, default=0)
    reservado: Mapped[int] = mapped_column(Integer, default=0)
    minimo_permitido: Mapped[int] = mapped_column(Integer, default=0)
