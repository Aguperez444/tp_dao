from typing import Annotated

from pydantic import Field

from app.application.dto.commands.transition_command import TransitionCommand
from app.infrastructure.api.dto.request.field_types import Name
from app.infrastructure.api.dto.request.input import Input


class TransitionInput(Input):
    responsable: Name
    observacion: Annotated[str, Field(max_length=500)] = ""
    codigo_precinto: Annotated[str, Field(max_length=60)] = ""
    numero_remito: Annotated[str, Field(max_length=50)] = ""
    precinto_intacto: bool = False
    contenido_conforme: bool = False

    def to_command(self) -> TransitionCommand:
        return TransitionCommand(
            responsable=self.responsable,
            observacion=self.observacion,
            codigo_precinto=self.codigo_precinto,
            numero_remito=self.numero_remito,
            precinto_intacto=self.precinto_intacto,
            contenido_conforme=self.contenido_conforme,
        )
