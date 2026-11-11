"""Strategy: selección externa de una política de precio para una venta."""
from abc import ABC, abstractmethod
from .money import discount_cents
from .errors import BusinessError


class PricingPolicy(ABC):
    @abstractmethod
    def discount(self, price_cents: int) -> int:
        """Devuelve el descuento monetario unitario en centavos."""


class ListPrice(PricingPolicy):
    def discount(self, price_cents: int) -> int:
        return 0


class TenPercentDiscount(PricingPolicy):
    def discount(self, price_cents: int) -> int:
        return discount_cents(price_cents, 10)


class PriceCalculator:
    def __init__(self, policy: PricingPolicy):
        self.policy = policy

    def calculate(self, price_cents: int) -> tuple[int, int]:
        discount = self.policy.discount(price_cents)
        return price_cents, discount


def policy_for(name: str) -> PricingPolicy:
    policies = {'lista': ListPrice, 'descuento_10': TenPercentDiscount}
    if name not in policies:
        raise BusinessError('Política de precio desconocida.')
    return policies[name]()
