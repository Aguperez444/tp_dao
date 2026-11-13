from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class AddressCommand:
    calle: str
    altura: str
    ciudad_id: int
