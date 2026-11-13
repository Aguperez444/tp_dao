from typing import Annotated, Literal

from pydantic import Field

from app.application.dto.commands.quote_command import QuoteCommand
from app.infrastructure.api.dto.request.field_types import Id
from app.infrastructure.api.dto.request.input import Input
from app.infrastructure.api.dto.request.line_input import LineInput


class QuoteInput(Input):
    local_id: Id
    politica: Literal["lista", "descuento_10"] = "lista"
    detalles: Annotated[list[LineInput], Field(min_length=1, max_length=100)]

    def to_command(self) -> QuoteCommand:
        return QuoteCommand(
            local_id=self.local_id,
            politica=self.politica,
            detalles=[item.to_command() for item in self.detalles],
        )
