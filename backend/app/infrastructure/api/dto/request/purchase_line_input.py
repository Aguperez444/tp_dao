from app.application.dto.commands.purchase_line_command import PurchaseLineCommand
from app.infrastructure.api.dto.request.field_types import Money
from app.infrastructure.api.dto.request.line_input import LineInput


class PurchaseLineInput(LineInput):
    costo: Money

    def to_command(self) -> PurchaseLineCommand:
        return PurchaseLineCommand(
            producto_id=self.producto_id, cantidad=self.cantidad, costo=self.costo
        )
