from app.application.dto.commands.named_command import NamedCommand
from app.infrastructure.api.dto.request.field_types import Name
from app.infrastructure.api.dto.request.input import Input


class NamedInput(Input):
    nombre: Name

    def to_command(self) -> NamedCommand:
        return NamedCommand(nombre=self.nombre)
