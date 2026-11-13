from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.estado_compra import EstadoCompra


@dataclass(kw_only=True)
class EstadoCompraObjectResponse:
    id: int
    nombre: str

    @classmethod
    def from_entity(cls, entity: EstadoCompra) -> Self:
        return cls(id=entity.id, nombre=entity.nombre)
