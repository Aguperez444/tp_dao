from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DetalleReposicionORM(Base):
    __tablename__ = "detalle_reposicion"
    __table_args__ = (
        UniqueConstraint("orden_id", "producto_id"),
        CheckConstraint("cantidad > 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"))
    orden_id: Mapped[int] = mapped_column(ForeignKey("orden_reposicion.id"))
    cantidad: Mapped[int] = mapped_column(Integer)
