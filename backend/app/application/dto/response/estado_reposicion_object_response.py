from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.estado_reposicion import EstadoReposicion


@dataclass(kw_only=True)
class EstadoReposicionObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: EstadoReposicion) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
