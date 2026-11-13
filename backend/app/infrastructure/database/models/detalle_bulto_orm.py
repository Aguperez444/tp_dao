from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DetalleBultoORM(Base):
    __tablename__ = "detalle_bulto"
    __table_args__ = (
        UniqueConstraint("bulto_id", "producto_id"),
        CheckConstraint("cantidad > 0"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("producto.id"))
    bulto_id: Mapped[int] = mapped_column(ForeignKey("bulto.id"))
    cantidad: Mapped[int] = mapped_column(Integer)
