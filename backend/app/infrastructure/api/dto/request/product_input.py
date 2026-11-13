from typing import Annotated

from pydantic import Field

from app.application.dto.commands.product_command import ProductCommand
from app.infrastructure.api.dto.request.field_types import Id, Money
from app.infrastructure.api.dto.request.named_input import NamedInput


class ProductInput(NamedInput):
    codigo: Annotated[str, Field(min_length=1, max_length=50)]
    detalle: Annotated[str, Field(max_length=1000)] = ""
    categoria_id: Id
    precio: Money
    costo_referencia: Money
    esta_activo: bool = True

    def to_command(self) -> ProductCommand:
        return ProductCommand(
            nombre=self.nombre,
            codigo=self.codigo,
            detalle=self.detalle,
            categoria_id=self.categoria_id,
            precio=self.precio,
            costo_referencia=self.costo_referencia,
            esta_activo=self.esta_activo,
        )
