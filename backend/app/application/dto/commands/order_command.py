from dataclasses import dataclass

from app.application.dto.commands.line_command import LineCommand


@dataclass(frozen=True, kw_only=True)
class OrderCommand:
    establecimiento_solicitante_id: int
    establecimiento_proveedor_id: int
    detalles: list[LineCommand]
