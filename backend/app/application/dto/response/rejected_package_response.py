from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class RejectedPackageResponse:
    destino: str
    bulto_id: int
    numero_remito: str
    fecha: str
    motivo: str
    unidades: int
    valor_referencia: int
