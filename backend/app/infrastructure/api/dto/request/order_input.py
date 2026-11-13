from typing import Annotated

from pydantic import Field

from app.application.dto.commands.order_command import OrderCommand
from app.infrastructure.api.dto.request.field_types import Id
from app.infrastructure.api.dto.request.input import Input
from app.infrastructure.api.dto.request.line_input import LineInput


class OrderInput(Input):
    establecimiento_solicitante_id: Id
    establecimiento_proveedor_id: Id
    detalles: Annotated[list[LineInput], Field(min_length=1, max_length=100)]

    def to_command(self) -> OrderCommand:
        return OrderCommand(
            establecimiento_solicitante_id=self.establecimiento_solicitante_id,
            establecimiento_proveedor_id=self.establecimiento_proveedor_id,
            detalles=[item.to_command() for item in self.detalles],
        )
