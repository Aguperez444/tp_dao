from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DetalleVentaORM(Base):
    __tablename__ = "detalle_venta"
    __table_args__ = (
        UniqueConstraint("venta_id", "producto_id"),
        CheckConstraint(
            "cantidad > 0 AND precio_unitario > 0 AND descuento_aplicado >= 0 AND descuento_aplicado < precio_unitario AND costo_unitario >= 0"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"))
    venta_id: Mapped[int] = mapped_column(ForeignKey("venta.id"))
    cantidad: Mapped[int] = mapped_column(Integer)
    precio_unitario: Mapped[int] = mapped_column(Integer)
    descuento_aplicado: Mapped[int] = mapped_column(Integer)
    costo_unitario: Mapped[int] = mapped_column(Integer)
