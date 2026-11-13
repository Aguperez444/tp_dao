from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.orden_reposicion import OrdenReposicion


@dataclass(kw_only=True)
class OrdenReposicionObjectResponse:
    id: int
    establecimiento_solicitante_id: int
    establecimiento_proveedor_id: int
    fecha: str
    estado_id: int

    @classmethod
    def from_entity(cls, entity: OrdenReposicion) -> Self:
        return cls(
            id=entity.id,
            establecimiento_solicitante_id=entity.establecimiento_solicitante_id,
            establecimiento_proveedor_id=entity.establecimiento_proveedor_id,
            fecha=entity.fecha,
            estado_id=entity.estado_id,
        )
