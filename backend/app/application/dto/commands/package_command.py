from dataclasses import dataclass

from app.application.dto.commands.line_command import LineCommand


@dataclass(frozen=True, kw_only=True)
class PackageCommand:
    responsable: str
    detalles: list[LineCommand]
