from __future__ import annotations

from app.application.dto.commands.quote_command import QuoteCommand
from app.application.dto.response.quote_line_response import QuoteLineResponse
from app.application.dto.response.sale_quote_response import SaleQuoteResponse
from app.application.ports.i_unit_of_work import IUnitOfWork
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.exceptions.business_error import BusinessError
from app.domain.services.pricing.policy_factory import policy_for
from app.domain.services.pricing.price_calculator import PriceCalculator


class SalePricingService:
    @staticmethod
    def quote(uow: IUnitOfWork, data: QuoteCommand) -> SaleQuoteResponse:
        EntityValidationService.local(uow.establecimiento_repo, data.local_id)
        calculator = PriceCalculator(policy_for(data.politica))
        lines = EntityValidationService.lines(uow.producto_repo, data.detalles)
        details = []
        for product_id, quantity in lines.items():
            product = EntityValidationService.require(uow.producto_repo, product_id)
            stocks = uow.existencia_repo.list(
                establecimiento_id=data.local_id, producto_id=product_id
            )
            available = (
                stocks[0].almacenado_total - stocks[0].reservado if stocks else 0
            )
            if available < quantity:
                raise BusinessError(
                    f"Stock disponible insuficiente para {product.nombre}: hay {available}."
                )
            price, discount = calculator.calculate(product.precio)
            details.append(
                QuoteLineResponse(
                    producto_id=product_id,
                    cantidad=quantity,
                    precio_unitario=price,
                    descuento_aplicado=discount,
                    costo_unitario=product.costo_referencia,
                )
            )
        total = sum(
            (
                line.cantidad * (line.precio_unitario - line.descuento_aplicado)
                for line in details
            )
        )
        if total > 99999999999:
            raise BusinessError(
                "El total supera el máximo admitido de $999.999.999,99 por venta."
            )
        return SaleQuoteResponse(detalles=details, total=total)
