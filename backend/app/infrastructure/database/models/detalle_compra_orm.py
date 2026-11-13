from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DetalleCompraORM(Base):
    __tablename__ = "detalle_compra"
    __table_args__ = (
        UniqueConstraint("compra_id", "producto_id"),
        CheckConstraint("cantidad > 0 AND costo >= 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"))
    compra_id: Mapped[int] = mapped_column(ForeignKey("compra.id"))
    cantidad: Mapped[int] = mapped_column(Integer)
    costo: Mapped[int] = mapped_column(Integer)
