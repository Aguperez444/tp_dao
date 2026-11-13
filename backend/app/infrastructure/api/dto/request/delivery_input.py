from typing import Annotated

from pydantic import Field

from app.application.dto.commands.delivery_command import DeliveryCommand
from app.infrastructure.api.dto.request.input import Input


class DeliveryInput(Input):
    numero_remito: Annotated[str, Field(min_length=1, max_length=50)]

    def to_command(self) -> DeliveryCommand:
        return DeliveryCommand(numero_remito=self.numero_remito)
