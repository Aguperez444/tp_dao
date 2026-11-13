from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.application.dto.response.refund_detail_response import RefundDetailResponse
from app.application.dto.response.sale_detail_line_response import (
    SaleDetailLineResponse,
)
from app.domain.models.venta import Venta


@dataclass(kw_only=True)
class SaleDetailResponse:
    id: int
    local_id: int
    metodo_pago_id: int
    total: int
    fecha: str
    numero_comprobante: str
    local: str
    metodo_pago: str
    reintegrado: int
    detalles: list[SaleDetailLineResponse]
    devoluciones: list[RefundDetailResponse]

    @classmethod
    def from_entity(
        cls,
        entity: Venta,
        *,
        local: str,
        metodo_pago: str,
        reintegrado: int,
        detalles: list[SaleDetailLineResponse],
        devoluciones: list[RefundDetailResponse],
    ) -> Self:
        return cls(
            id=entity.id,
            local_id=entity.local_id,
            metodo_pago_id=entity.metodo_pago_id,
            total=entity.total,
            fecha=entity.fecha,
            numero_comprobante=entity.numero_comprobante,
            local=local,
            metodo_pago=metodo_pago,
            reintegrado=reintegrado,
            detalles=detalles,
            devoluciones=devoluciones,
        )
