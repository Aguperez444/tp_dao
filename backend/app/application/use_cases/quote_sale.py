from __future__ import annotations

from app.application.dto.commands.quote_command import QuoteCommand
from app.application.dto.response.sale_quote_response import SaleQuoteResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.sale_pricing_service import SalePricingService


class QuoteSale:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, data: QuoteCommand) -> SaleQuoteResponse:
        with self.uow_factory() as uow:
            return SalePricingService.quote(uow, data)
