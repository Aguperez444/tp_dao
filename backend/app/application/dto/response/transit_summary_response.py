from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class TransitSummaryResponse:
    destino: str
    recibidos: int
    horas_promedio: float | None
    en_transito: int
