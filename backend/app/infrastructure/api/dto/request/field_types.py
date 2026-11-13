from decimal import Decimal
from typing import Annotated

from pydantic import Field

Id = Annotated[int, Field(gt=0, strict=True)]
Quantity = Annotated[int, Field(gt=0, le=1_000_000, strict=True)]
Money = Annotated[Decimal, Field(ge=0, le=Decimal("999999999.99"), decimal_places=2)]
Name = Annotated[str, Field(min_length=1, max_length=150)]
