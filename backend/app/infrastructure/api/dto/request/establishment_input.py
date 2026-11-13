from app.application.dto.commands.establishment_command import EstablishmentCommand
from app.infrastructure.api.dto.request.field_types import Id
from app.infrastructure.api.dto.request.named_input import NamedInput


class EstablishmentInput(NamedInput):
    es_central: bool = False
    domicilio_id: Id

    def to_command(self) -> EstablishmentCommand:
        return EstablishmentCommand(
            nombre=self.nombre,
            es_central=self.es_central,
            domicilio_id=self.domicilio_id,
        )
