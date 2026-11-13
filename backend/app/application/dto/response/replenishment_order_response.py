from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.application.dto.response.delivery_detail_response import DeliveryDetailResponse
from app.application.dto.response.replenishment_line_response import (
    ReplenishmentLineResponse,
)
from app.domain.models.orden_reposicion import OrdenReposicion


@dataclass(kw_only=True)
class ReplenishmentOrderResponse:
    id: int
    establecimiento_solicitante_id: int
    establecimiento_proveedor_id: int
    fecha: str
    estado_id: int
    origen: str
    destino: str
    estado: str
    detalles: list[ReplenishmentLineResponse]
    remitos: list[DeliveryDetailResponse]

    @classmethod
    def from_entity(
        cls,
        entity: OrdenReposicion,
        *,
        origen: str,
        destino: str,
        estado: str,
        detalles: list[ReplenishmentLineResponse],
        remitos: list[DeliveryDetailResponse],
    ) -> Self:
        return cls(
            id=entity.id,
            establecimiento_solicitante_id=entity.establecimiento_solicitante_id,
            establecimiento_proveedor_id=entity.establecimiento_proveedor_id,
            fecha=entity.fecha,
            estado_id=entity.estado_id,
            origen=origen,
            destino=destino,
            estado=estado,
            detalles=detalles,
            remitos=remitos,
        )
