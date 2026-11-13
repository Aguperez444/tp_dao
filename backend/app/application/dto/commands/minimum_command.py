from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class MinimumCommand:
    establecimiento_id: int
    producto_id: int
    minimo_permitido: int
