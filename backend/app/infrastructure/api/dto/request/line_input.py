from app.application.dto.commands.line_command import LineCommand
from app.infrastructure.api.dto.request.field_types import Id, Quantity
from app.infrastructure.api.dto.request.input import Input


class LineInput(Input):
    producto_id: Id
    cantidad: Quantity

    def to_command(self) -> LineCommand:
        return LineCommand(producto_id=self.producto_id, cantidad=self.cantidad)
