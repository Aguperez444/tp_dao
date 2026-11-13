from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class BultoORM(Base):
    __tablename__ = "bulto"
    id: Mapped[int] = mapped_column(primary_key=True)
    remito_id: Mapped[int] = mapped_column(ForeignKey("remito.id"))
    estado_precinto_id: Mapped[int] = mapped_column(ForeignKey("estado_precinto.id"))
    estado_bulto_id: Mapped[int] = mapped_column(ForeignKey("estado_bulto.id"))
    codigo_precinto: Mapped[str | None] = mapped_column(String(60), unique=True)
