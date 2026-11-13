from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class StockItemResponse:
    establecimiento_id: int
    establecimiento: str
    producto_id: int
    codigo: str
    producto: str
    almacenado_total: int
    reservado: int
    disponible: int
    minimo_permitido: int
    faltante: int
    valorizacion: int
