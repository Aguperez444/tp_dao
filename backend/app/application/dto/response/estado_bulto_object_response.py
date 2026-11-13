from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.estado_bulto import EstadoBulto


@dataclass(kw_only=True)
class EstadoBultoObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: EstadoBulto) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
