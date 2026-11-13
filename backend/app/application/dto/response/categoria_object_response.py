from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.categoria import Categoria


@dataclass(kw_only=True)
class CategoriaObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: Categoria) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
