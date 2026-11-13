from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class VentaORM(Base):
    __tablename__ = "venta"
    __table_args__ = (CheckConstraint("total > 0"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    local_id: Mapped[int] = mapped_column(ForeignKey("establecimiento.id"))
    metodo_pago_id: Mapped[int] = mapped_column(ForeignKey("metodo_pago.id"))
    total: Mapped[int] = mapped_column(Integer)
    fecha: Mapped[str] = mapped_column(String(40), index=True)
    numero_comprobante: Mapped[str] = mapped_column(String(50), unique=True)
