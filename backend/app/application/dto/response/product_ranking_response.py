from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class ProductRankingResponse:
    codigo: str
    producto: str
    unidades_netas: int
    ingreso_neto: int
    costo_neto: int
    margen_estimado: int
