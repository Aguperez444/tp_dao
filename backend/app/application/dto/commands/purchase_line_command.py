from dataclasses import dataclass
from decimal import Decimal

from app.application.dto.commands.line_command import LineCommand


@dataclass(frozen=True, kw_only=True)
class PurchaseLineCommand(LineCommand):
    costo: Decimal | str | int
