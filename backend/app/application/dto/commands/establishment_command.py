from dataclasses import dataclass

from app.application.dto.commands.named_command import NamedCommand


@dataclass(frozen=True, kw_only=True)
class EstablishmentCommand(NamedCommand):
    es_central: bool = False
    domicilio_id: int
