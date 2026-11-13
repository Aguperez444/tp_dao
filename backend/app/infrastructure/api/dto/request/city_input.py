from app.application.dto.commands.city_command import CityCommand
from app.infrastructure.api.dto.request.field_types import Id
from app.infrastructure.api.dto.request.named_input import NamedInput


class CityInput(NamedInput):
    provincia_id: Id

    def to_command(self) -> CityCommand:
        return CityCommand(nombre=self.nombre, provincia_id=self.provincia_id)
