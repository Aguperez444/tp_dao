from dataclasses import dataclass

from app.application.dto.commands.purchase_line_command import PurchaseLineCommand


@dataclass(frozen=True, kw_only=True)
class PurchaseCommand:
    proveedor_id: int
    detalles: list[PurchaseLineCommand]
