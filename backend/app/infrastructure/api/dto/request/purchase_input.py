from typing import Annotated

from pydantic import Field

from app.application.dto.commands.purchase_command import PurchaseCommand
from app.infrastructure.api.dto.request.field_types import Id
from app.infrastructure.api.dto.request.input import Input
from app.infrastructure.api.dto.request.purchase_line_input import PurchaseLineInput


class PurchaseInput(Input):
    proveedor_id: Id
    detalles: Annotated[list[PurchaseLineInput], Field(min_length=1, max_length=100)]

    def to_command(self) -> PurchaseCommand:
        return PurchaseCommand(
            proveedor_id=self.proveedor_id,
            detalles=[item.to_command() for item in self.detalles],
        )
