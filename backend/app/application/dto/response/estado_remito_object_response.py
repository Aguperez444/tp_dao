from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.estado_remito import EstadoRemito


@dataclass(kw_only=True)
class EstadoRemitoObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: EstadoRemito) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
