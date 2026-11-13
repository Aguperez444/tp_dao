from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.producto import Producto


@dataclass(kw_only=True)
class ProductoObjectResponse:
    id: int
    nombre: str
    detalle: str
    categoria_id: int
    precio: int
    costo_referencia: int
    esta_activo: bool
    codigo: str

    @classmethod
    def from_entity(cls, entity: Producto) -> Self:
        return cls(
            id=entity.id,
            nombre=entity.nombre,
            detalle=entity.detalle,
            categoria_id=entity.categoria_id,
            precio=entity.precio,
            costo_referencia=entity.costo_referencia,
            esta_activo=entity.esta_activo,
            codigo=entity.codigo,
        )
