from dataclasses import dataclass
from typing import Literal

from app.application.dto.commands.line_command import LineCommand


@dataclass(frozen=True, kw_only=True)
class QuoteCommand:
    local_id: int
    politica: Literal["lista", "descuento_10"] = "lista"
    detalles: list[LineCommand]
