from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.detalle_devolucion import DetalleDevolucion


@dataclass(kw_only=True)
class DetalleDevolucionObjectResponse:
    id: int
    producto_id: int
    devolucion_id: int
    cantidad: int
    importe_unitario: int

    @classmethod
    def from_entity(cls, entity: DetalleDevolucion) -> Self:
        return cls(
            id=entity.id,
            producto_id=entity.producto_id,
            devolucion_id=entity.devolucion_id,
            cantidad=entity.cantidad,
            importe_unitario=entity.importe_unitario,
        )
