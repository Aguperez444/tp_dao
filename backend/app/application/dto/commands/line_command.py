from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class LineCommand:
    producto_id: int
    cantidad: int
