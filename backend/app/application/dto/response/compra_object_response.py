from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.compra import Compra


@dataclass(kw_only=True)
class CompraObjectResponse:
    id: int
    proveedor_id: int
    estado_id: int
    fecha: str

    @classmethod
    def from_entity(cls, entity: Compra) -> Self:
        return cls(
            id=entity.id,
            proveedor_id=entity.proveedor_id,
            estado_id=entity.estado_id,
            fecha=entity.fecha,
        )
