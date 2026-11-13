from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.application.dto.response.detalle_bulto_object_response import (
    DetalleBultoObjectResponse,
)
from app.application.dto.response.package_event_response import PackageEventResponse
from app.domain.models.bulto import Bulto


@dataclass(kw_only=True)
class PackageDetailResponse:
    id: int
    remito_id: int
    estado_precinto_id: int
    estado_bulto_id: int
    codigo_precinto: str | None
    estado: str
    estado_precinto: str
    detalles: list[DetalleBultoObjectResponse]
    historial: list[PackageEventResponse]

    @classmethod
    def from_entity(
        cls,
        entity: Bulto,
        *,
        estado: str,
        estado_precinto: str,
        detalles: list[DetalleBultoObjectResponse],
        historial: list[PackageEventResponse],
    ) -> Self:
        return cls(
            id=entity.id,
            remito_id=entity.remito_id,
            estado_precinto_id=entity.estado_precinto_id,
            estado_bulto_id=entity.estado_bulto_id,
            codigo_precinto=entity.codigo_precinto,
            estado=estado,
            estado_precinto=estado_precinto,
            detalles=detalles,
            historial=historial,
        )
