from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.response.quote_line_response import QuoteLineResponse


@dataclass(kw_only=True)
class SaleQuoteResponse:
    detalles: list[QuoteLineResponse]
    total: int
