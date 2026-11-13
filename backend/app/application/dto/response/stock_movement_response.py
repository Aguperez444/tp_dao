from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class StockMovementResponse:
    fecha: str
    establecimiento: str
    codigo: str
    producto: str
    cantidad: int
    concepto: str
    referencia: str
