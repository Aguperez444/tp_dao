from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.application.dto.response.detalle_compra_object_response import (
    DetalleCompraObjectResponse,
)
from app.domain.models.compra import Compra


@dataclass(kw_only=True)
class PurchaseSummaryResponse:
    id: int
    proveedor_id: int
    estado_id: int
    fecha: str
    estado: str
    proveedor: str
    total: int
    detalles: list[DetalleCompraObjectResponse]

    @classmethod
    def from_entity(
        cls,
        entity: Compra,
        *,
        estado: str,
        proveedor: str,
        total: int,
        detalles: list[DetalleCompraObjectResponse],
    ) -> Self:
        return cls(
            id=entity.id,
            proveedor_id=entity.proveedor_id,
            estado_id=entity.estado_id,
            fecha=entity.fecha,
            estado=estado,
            proveedor=proveedor,
            total=total,
            detalles=detalles,
        )
