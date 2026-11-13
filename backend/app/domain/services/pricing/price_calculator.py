from app.domain.services.pricing.pricing_policy import PricingPolicy


class PriceCalculator:
    def __init__(self, policy: PricingPolicy) -> None:
        self.policy = policy

    def calculate(self, price_cents: int) -> tuple[int, int]:
        discount = self.policy.discount(price_cents)
        return price_cents, discount
