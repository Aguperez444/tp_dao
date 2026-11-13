from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.response.product_ranking_response import ProductRankingResponse
from app.application.dto.response.rejected_package_response import (
    RejectedPackageResponse,
)
from app.application.dto.response.sales_by_payment_response import (
    SalesByPaymentResponse,
)
from app.application.dto.response.stock_item_response import StockItemResponse
from app.application.dto.response.transit_summary_response import TransitSummaryResponse


@dataclass(kw_only=True)
class ReportDataResponse:
    ventas: list[SalesByPaymentResponse]
    productos: list[ProductRankingResponse]
    existencias: list[StockItemResponse]
    rechazos: list[RejectedPackageResponse]
    transito: list[TransitSummaryResponse]
