from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.application.dto.response.package_detail_response import PackageDetailResponse
from app.domain.models.remito import Remito


@dataclass(kw_only=True)
class DeliveryDetailResponse:
    id: int
    orden_reposicion_id: int
    estado_remito_id: int
    numero_remito: str
    fecha_emision: str
    estado: str
    bultos: list[PackageDetailResponse]

    @classmethod
    def from_entity(
        cls, entity: Remito, *, estado: str, bultos: list[PackageDetailResponse]
    ) -> Self:
        return cls(
            id=entity.id,
            orden_reposicion_id=entity.orden_reposicion_id,
            estado_remito_id=entity.estado_remito_id,
            numero_remito=entity.numero_remito,
            fecha_emision=entity.fecha_emision,
            estado=estado,
            bultos=bultos,
        )
