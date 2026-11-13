from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class RemitoORM(Base):
    __tablename__ = "remito"
    id: Mapped[int] = mapped_column(primary_key=True)
    orden_reposicion_id: Mapped[int] = mapped_column(ForeignKey("orden_reposicion.id"))
    estado_remito_id: Mapped[int] = mapped_column(ForeignKey("estado_remito.id"))
    numero_remito: Mapped[str] = mapped_column(String(50), unique=True)
    fecha_emision: Mapped[str] = mapped_column(String(40))
