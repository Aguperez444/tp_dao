from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.detalle_venta import DetalleVenta


@dataclass(kw_only=True)
class SaleDetailLineResponse:
    id: int
    producto_id: int
    venta_id: int
    cantidad: int
    precio_unitario: int
    descuento_aplicado: int
    costo_unitario: int
    producto: str
    devuelta: int
    subtotal: int

    @classmethod
    def from_entity(
        cls, entity: DetalleVenta, *, producto: str, devuelta: int, subtotal: int
    ) -> Self:
        return cls(
            id=entity.id,
            producto_id=entity.producto_id,
            venta_id=entity.venta_id,
            cantidad=entity.cantidad,
            precio_unitario=entity.precio_unitario,
            descuento_aplicado=entity.descuento_aplicado,
            costo_unitario=entity.costo_unitario,
            producto=producto,
            devuelta=devuelta,
            subtotal=subtotal,
        )
