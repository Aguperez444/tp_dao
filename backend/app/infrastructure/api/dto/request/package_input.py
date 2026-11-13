from typing import Annotated

from pydantic import Field

from app.application.dto.commands.package_command import PackageCommand
from app.infrastructure.api.dto.request.field_types import Name
from app.infrastructure.api.dto.request.input import Input
from app.infrastructure.api.dto.request.line_input import LineInput


class PackageInput(Input):
    responsable: Name
    detalles: Annotated[list[LineInput], Field(min_length=1, max_length=100)]

    def to_command(self) -> PackageCommand:
        return PackageCommand(
            responsable=self.responsable,
            detalles=[item.to_command() for item in self.detalles],
        )
