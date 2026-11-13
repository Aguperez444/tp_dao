from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.detalle_bulto import DetalleBulto


@dataclass(kw_only=True)
class DetalleBultoObjectResponse:
    id: int
    producto_id: int
    bulto_id: int
    cantidad: int

    @classmethod
    def from_entity(cls, entity: DetalleBulto) -> Self:
        return cls(
            id=entity.id,
            producto_id=entity.producto_id,
            bulto_id=entity.bulto_id,
            cantidad=entity.cantidad,
        )
