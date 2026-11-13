from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class CiudadORM(Base):
    __tablename__ = "ciudad"
    __table_args__ = (UniqueConstraint("nombre", "provincia_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincia.id"))
