from dataclasses import dataclass

from app.application.dto.commands.line_command import LineCommand


@dataclass(frozen=True, kw_only=True)
class RefundCommand:
    motivo_id: int
    metodo_reintegro_id: int
    detalle: str
    productos_aptos: bool
    detalles: list[LineCommand]
