from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.proveedor import Proveedor


@dataclass(kw_only=True)
class ProveedorObjectResponse:
    id: int
    CUIT: str
    nombre: str
    esta_activo: bool

    @classmethod
    def from_entity(cls, entity: Proveedor) -> Self:
        return cls(
            id=entity.id,
            CUIT=entity.CUIT,
            nombre=entity.nombre,
            esta_activo=entity.esta_activo,
        )
