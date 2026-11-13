from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.detalle_reposicion import DetalleReposicion


@dataclass(kw_only=True)
class ReplenishmentLineResponse:
    id: int
    producto_id: int
    orden_id: int
    cantidad: int
    asignada: int

    @classmethod
    def from_entity(cls, entity: DetalleReposicion, *, asignada: int) -> Self:
        return cls(
            id=entity.id,
            producto_id=entity.producto_id,
            orden_id=entity.orden_id,
            cantidad=entity.cantidad,
            asignada=asignada,
        )
