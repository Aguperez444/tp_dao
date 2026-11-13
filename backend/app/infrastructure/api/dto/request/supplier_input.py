from typing import Annotated

from pydantic import Field

from app.application.dto.commands.supplier_command import SupplierCommand
from app.infrastructure.api.dto.request.named_input import NamedInput


class SupplierInput(NamedInput):
    CUIT: Annotated[str, Field(min_length=11, max_length=20)]
    esta_activo: bool = True

    def to_command(self) -> SupplierCommand:
        return SupplierCommand(
            nombre=self.nombre, CUIT=self.CUIT, esta_activo=self.esta_activo
        )
