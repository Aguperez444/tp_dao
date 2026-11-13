from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.venta import Venta


@dataclass(kw_only=True)
class VentaObjectResponse:
    id: int
    local_id: int
    metodo_pago_id: int
    total: int
    fecha: str
    numero_comprobante: str

    @classmethod
    def from_entity(cls, entity: Venta) -> Self:
        return cls(
            id=entity.id,
            local_id=entity.local_id,
            metodo_pago_id=entity.metodo_pago_id,
            total=entity.total,
            fecha=entity.fecha,
            numero_comprobante=entity.numero_comprobante,
        )
