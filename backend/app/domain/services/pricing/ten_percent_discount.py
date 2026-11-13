from app.domain.services.money_service import discount_cents
from app.domain.services.pricing.pricing_policy import PricingPolicy


class TenPercentDiscount(PricingPolicy):
    def discount(self, price_cents: int) -> int:
        return discount_cents(price_cents, 10)
