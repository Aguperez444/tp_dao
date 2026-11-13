from dataclasses import dataclass

from app.application.dto.commands.named_command import NamedCommand


@dataclass(frozen=True, kw_only=True)
class SupplierCommand(NamedCommand):
    CUIT: str
    esta_activo: bool = True
