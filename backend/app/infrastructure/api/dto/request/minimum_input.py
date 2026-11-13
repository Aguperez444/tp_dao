from typing import Annotated

from pydantic import Field

from app.application.dto.commands.minimum_command import MinimumCommand
from app.infrastructure.api.dto.request.field_types import Id
from app.infrastructure.api.dto.request.input import Input


class MinimumInput(Input):
    establecimiento_id: Id
    producto_id: Id
    minimo_permitido: Annotated[int, Field(ge=0, le=1_000_000, strict=True)]

    def to_command(self) -> MinimumCommand:
        return MinimumCommand(
            establecimiento_id=self.establecimiento_id,
            producto_id=self.producto_id,
            minimo_permitido=self.minimo_permitido,
        )
