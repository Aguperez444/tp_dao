from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.ciudad import Ciudad


@dataclass(kw_only=True)
class CiudadObjectResponse:
    id: int
    nombre: str
    provincia_id: int

    @classmethod
    def from_entity(cls, entity: Ciudad) -> Self:
        return cls(id=entity.id, nombre=entity.nombre, provincia_id=entity.provincia_id)
