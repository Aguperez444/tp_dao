from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.cambio_estado_bulto import CambioEstadoBulto


@dataclass(kw_only=True)
class PackageEventResponse:
    id: int
    bulto_id: int
    estado_bulto_id: int
    fecha: str
    responsable: str
    observacion: str
    estado: str

    @classmethod
    def from_entity(cls, entity: CambioEstadoBulto, *, estado: str) -> Self:
        return cls(
            id=entity.id,
            bulto_id=entity.bulto_id,
            estado_bulto_id=entity.estado_bulto_id,
            fecha=entity.fecha,
            responsable=entity.responsable,
            observacion=entity.observacion,
            estado=estado,
        )
