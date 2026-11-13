from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DetalleDevolucionORM(Base):
    __tablename__ = "detalle_devolucion"
    __table_args__ = (
        UniqueConstraint("devolucion_id", "producto_id"),
        CheckConstraint("cantidad > 0 AND importe_unitario >= 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"))
    devolucion_id: Mapped[int] = mapped_column(ForeignKey("devolucion.id"))
    cantidad: Mapped[int] = mapped_column(Integer)
    importe_unitario: Mapped[int] = mapped_column(Integer)
