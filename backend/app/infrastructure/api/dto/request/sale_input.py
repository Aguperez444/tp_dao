from app.application.dto.commands.sale_command import SaleCommand
from app.infrastructure.api.dto.request.field_types import Id, Money
from app.infrastructure.api.dto.request.quote_input import QuoteInput


class SaleInput(QuoteInput):
    metodo_pago_id: Id
    importe_cobrado: Money

    def to_command(self) -> SaleCommand:
        return SaleCommand(
            local_id=self.local_id,
            politica=self.politica,
            detalles=[item.to_command() for item in self.detalles],
            metodo_pago_id=self.metodo_pago_id,
            importe_cobrado=self.importe_cobrado,
        )
