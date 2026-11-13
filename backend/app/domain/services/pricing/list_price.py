from app.domain.services.pricing.pricing_policy import PricingPolicy


class ListPrice(PricingPolicy):
    def discount(self, price_cents: int) -> int:
        return 0
