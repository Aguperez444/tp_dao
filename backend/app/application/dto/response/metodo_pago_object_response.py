from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.metodo_pago import MetodoPago


@dataclass(kw_only=True)
class MetodoPagoObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: MetodoPago) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
