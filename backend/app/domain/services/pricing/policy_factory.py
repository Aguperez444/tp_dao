from app.domain.exceptions.business_error import BusinessError
from app.domain.services.pricing.list_price import ListPrice
from app.domain.services.pricing.pricing_policy import PricingPolicy
from app.domain.services.pricing.ten_percent_discount import TenPercentDiscount


def policy_for(name: str) -> PricingPolicy:
    policies = {"lista": ListPrice, "descuento_10": TenPercentDiscount}
    if name not in policies:
        raise BusinessError("Política de precio desconocida.")
    return policies[name]()
