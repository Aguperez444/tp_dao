from abc import ABC, abstractmethod


class PricingPolicy(ABC):
    @abstractmethod
    def discount(self, price_cents: int) -> int:
        """Devuelve el descuento monetario unitario en centavos."""
