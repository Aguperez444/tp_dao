from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from app.domain.models.domicilio import Domicilio


@dataclass(kw_only=True)
class DomicilioObjectResponse:
    id: int
    calle: str
    altura: str
    ciudad_id: int

    @classmethod
    def from_entity(cls, entity: Domicilio) -> Self:
        return cls(
            id=entity.id,
            calle=entity.calle,
            altura=entity.altura,
            ciudad_id=entity.ciudad_id,
        )
