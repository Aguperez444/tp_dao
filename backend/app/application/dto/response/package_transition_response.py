from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.bulto import Bulto


@dataclass(kw_only=True)
class PackageTransitionResponse:
    id: int
    remito_id: int
    estado_precinto_id: int
    estado_bulto_id: int
    codigo_precinto: str | None
    estado: str

    @classmethod
    def from_entity(cls, entity: Bulto, *, estado: str) -> Self:
        return cls(
            id=entity.id,
            remito_id=entity.remito_id,
            estado_precinto_id=entity.estado_precinto_id,
            estado_bulto_id=entity.estado_bulto_id,
            codigo_precinto=entity.codigo_precinto,
            estado=estado,
        )
