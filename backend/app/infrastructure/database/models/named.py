from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Named:
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
