from typing import Annotated

from pydantic import Field

from app.application.dto.commands.refund_command import RefundCommand
from app.infrastructure.api.dto.request.field_types import Id
from app.infrastructure.api.dto.request.input import Input
from app.infrastructure.api.dto.request.line_input import LineInput


class RefundInput(Input):
    motivo_id: Id
    metodo_reintegro_id: Id
    detalle: Annotated[str, Field(min_length=1, max_length=500)]
    productos_aptos: bool
    detalles: Annotated[list[LineInput], Field(min_length=1, max_length=100)]

    def to_command(self) -> RefundCommand:
        return RefundCommand(
            motivo_id=self.motivo_id,
            metodo_reintegro_id=self.metodo_reintegro_id,
            detalle=self.detalle,
            productos_aptos=self.productos_aptos,
            detalles=[item.to_command() for item in self.detalles],
        )
