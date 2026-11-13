from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.application.dto.response.detalle_devolucion_object_response import (
    DetalleDevolucionObjectResponse,
)
from app.domain.models.devolucion import Devolucion


@dataclass(kw_only=True)
class RefundDetailResponse:
    id: int
    venta_id: int
    motivo_id: int
    metodo_reintegro_id: int
    detalle: str
    fecha: str
    numero_comprobante: str
    motivo: str
    metodo_reintegro: str
    total: int
    detalles: list[DetalleDevolucionObjectResponse]

    @classmethod
    def from_entity(
        cls,
        entity: Devolucion,
        *,
        numero_comprobante: str,
        motivo: str,
        metodo_reintegro: str,
        total: int,
        detalles: list[DetalleDevolucionObjectResponse],
    ) -> Self:
        return cls(
            id=entity.id,
            venta_id=entity.venta_id,
            motivo_id=entity.motivo_id,
            metodo_reintegro_id=entity.metodo_reintegro_id,
            detalle=entity.detalle,
            fecha=entity.fecha,
            numero_comprobante=numero_comprobante,
            motivo=motivo,
            metodo_reintegro=metodo_reintegro,
            total=total,
            detalles=detalles,
        )
