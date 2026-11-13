from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.provincia import Provincia


@dataclass(kw_only=True)
class ProvinciaObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: Provincia) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
