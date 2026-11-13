from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.motivo import Motivo


@dataclass(kw_only=True)
class MotivoObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: Motivo) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
