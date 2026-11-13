from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class SalesByPaymentResponse:
    local: str
    medio_pago: str
    bruto: int
    reintegros: int
    neto: int
