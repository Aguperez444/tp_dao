from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.detalle_compra import DetalleCompra


@dataclass(kw_only=True)
class DetalleCompraObjectResponse:
    id: int
    producto_id: int
    compra_id: int
    cantidad: int
    costo: int

    @classmethod
    def from_entity(cls, entity: DetalleCompra) -> Self:
        return cls(
            id=entity.id,
            producto_id=entity.producto_id,
            compra_id=entity.compra_id,
            cantidad=entity.cantidad,
            costo=entity.costo,
        )
