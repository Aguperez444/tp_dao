from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class OrdenReposicionORM(Base):
    __tablename__ = "orden_reposicion"
    __table_args__ = (
        CheckConstraint(
            "establecimiento_solicitante_id <> establecimiento_proveedor_id"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    establecimiento_solicitante_id: Mapped[int] = mapped_column(
        ForeignKey("establecimiento.id")
    )
    establecimiento_proveedor_id: Mapped[int] = mapped_column(
        ForeignKey("establecimiento.id")
    )
    fecha: Mapped[str] = mapped_column(String(40))
    estado_id: Mapped[int] = mapped_column(ForeignKey("estado_reposicion.id"))
