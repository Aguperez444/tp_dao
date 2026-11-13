from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DomicilioORM(Base):
    __tablename__ = "domicilio"
    id: Mapped[int] = mapped_column(primary_key=True)
    calle: Mapped[str] = mapped_column(String(150))
    altura: Mapped[str] = mapped_column(String(30))
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudad.id"))
