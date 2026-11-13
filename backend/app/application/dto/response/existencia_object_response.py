from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.existencia import Existencia


@dataclass(kw_only=True)
class ExistenciaObjectResponse:
    id: int
    establecimiento_id: int
    producto_id: int
    almacenado_total: int
    reservado: int
    minimo_permitido: int

    @classmethod
    def from_entity(cls, entity: Existencia) -> Self:
        return cls(
            id=entity.id,
            establecimiento_id=entity.establecimiento_id,
            producto_id=entity.producto_id,
            almacenado_total=entity.almacenado_total,
            reservado=entity.reservado,
            minimo_permitido=entity.minimo_permitido,
        )
