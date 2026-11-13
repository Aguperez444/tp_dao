from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DevolucionORM(Base):
    __tablename__ = "devolucion"
    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("venta.id"))
    motivo_id: Mapped[int] = mapped_column(ForeignKey("motivo.id"))
    metodo_reintegro_id: Mapped[int] = mapped_column(ForeignKey("metodo_pago.id"))
    detalle: Mapped[str] = mapped_column(String(500))
    fecha: Mapped[str] = mapped_column(String(40), index=True)
