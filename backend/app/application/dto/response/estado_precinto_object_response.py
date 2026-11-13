from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.estado_precinto import EstadoPrecinto


@dataclass(kw_only=True)
class EstadoPrecintoObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: EstadoPrecinto) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
