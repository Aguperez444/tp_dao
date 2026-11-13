from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class CompraORM(Base):
    __tablename__ = "compra"
    id: Mapped[int] = mapped_column(primary_key=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedor.id"))
    estado_id: Mapped[int] = mapped_column(ForeignKey("estado_compra.id"))
    fecha: Mapped[str] = mapped_column(String(40))
