from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from .errors import BusinessError

MAX_AMOUNT = Decimal('999999999.99')


def to_cents(value: Decimal | str | int) -> int:
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0 or amount > MAX_AMOUNT:
            raise InvalidOperation
        if amount != amount.quantize(Decimal('.01')):
            raise BusinessError('Los importes admiten hasta dos decimales.')
        return int(amount * 100)
    except (InvalidOperation, ValueError):
        raise BusinessError('Importe inválido: use pesos con hasta dos decimales.') from None


def discount_cents(cents: int, percent: int) -> int:
    return int((Decimal(cents) * percent / 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
