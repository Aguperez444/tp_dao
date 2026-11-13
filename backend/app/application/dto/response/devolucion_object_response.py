from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.devolucion import Devolucion


@dataclass(kw_only=True)
class DevolucionObjectResponse:
    id: int
    venta_id: int
    motivo_id: int
    metodo_reintegro_id: int
    detalle: str
    fecha: str

    @classmethod
    def from_entity(cls, entity: Devolucion) -> Self:
        return cls(
            id=entity.id,
            venta_id=entity.venta_id,
            motivo_id=entity.motivo_id,
            metodo_reintegro_id=entity.metodo_reintegro_id,
            detalle=entity.detalle,
            fecha=entity.fecha,
        )
