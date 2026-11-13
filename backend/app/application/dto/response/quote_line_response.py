from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class QuoteLineResponse:
    producto_id: int
    cantidad: int
    precio_unitario: int
    descuento_aplicado: int
    costo_unitario: int
