from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class RefundLine:
    producto_id: int
    cantidad: int
    importe_unitario: int
