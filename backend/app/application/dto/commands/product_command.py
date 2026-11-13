from dataclasses import dataclass
from decimal import Decimal

from app.application.dto.commands.named_command import NamedCommand


@dataclass(frozen=True, kw_only=True)
class ProductCommand(NamedCommand):
    codigo: str
    detalle: str = ""
    categoria_id: int
    precio: Decimal | str | int
    costo_referencia: Decimal | str | int
    esta_activo: bool = True
