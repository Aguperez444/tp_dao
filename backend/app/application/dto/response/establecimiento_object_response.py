from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.establecimiento import Establecimiento


@dataclass(kw_only=True)
class EstablecimientoObjectResponse:
    id: int
    nombre: str
    es_central: bool
    domicilio_id: int

    @classmethod
    def from_entity(cls, entity: Establecimiento) -> Self:
        return cls(
            id=entity.id,
            nombre=entity.nombre,
            es_central=entity.es_central,
            domicilio_id=entity.domicilio_id,
        )
