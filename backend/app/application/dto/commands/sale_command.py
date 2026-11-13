from dataclasses import dataclass
from decimal import Decimal

from app.application.dto.commands.quote_command import QuoteCommand


@dataclass(frozen=True, kw_only=True)
class SaleCommand(QuoteCommand):
    metodo_pago_id: int
    importe_cobrado: Decimal | str | int
