from sqlalchemy import Boolean, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class EstablecimientoORM(Base):
    __tablename__ = "establecimiento"
    __table_args__ = (
        Index(
            "unico_centro",
            "es_central",
            unique=True,
            sqlite_where=text("es_central = 1"),
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True)
    es_central: Mapped[bool] = mapped_column(Boolean, default=False)
    domicilio_id: Mapped[int] = mapped_column(ForeignKey("domicilio.id"))
