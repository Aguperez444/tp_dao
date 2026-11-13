from typing import Annotated

from pydantic import Field

from app.application.dto.commands.address_command import AddressCommand
from app.infrastructure.api.dto.request.field_types import Id, Name
from app.infrastructure.api.dto.request.input import Input


class AddressInput(Input):
    calle: Name
    altura: Annotated[str, Field(min_length=1, max_length=30)]
    ciudad_id: Id

    def to_command(self) -> AddressCommand:
        return AddressCommand(
            calle=self.calle, altura=self.altura, ciudad_id=self.ciudad_id
        )
