from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class CambioEstadoBultoORM(Base):
    __tablename__ = "cambio_estado_bulto"
    id: Mapped[int] = mapped_column(primary_key=True)
    bulto_id: Mapped[int] = mapped_column(ForeignKey("bulto.id"), index=True)
    estado_bulto_id: Mapped[int] = mapped_column(ForeignKey("estado_bulto.id"))
    fecha: Mapped[str] = mapped_column(String(40))
    responsable: Mapped[str] = mapped_column(String(150))
    observacion: Mapped[str] = mapped_column(String(500))
