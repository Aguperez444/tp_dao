from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class DeliveryCommand:
    numero_remito: str
