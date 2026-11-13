from fastapi import APIRouter, Request

from app.application.dto.response.sale_detail_response import SaleDetailResponse
from app.application.dto.response.sale_quote_response import SaleQuoteResponse
from app.application.dto.response.sale_summary_response import SaleSummaryResponse
from app.application.use_cases.create_sale import CreateSale
from app.application.use_cases.get_sale import GetSale
from app.application.use_cases.query_sales import QuerySales
from app.application.use_cases.quote_sale import QuoteSale
from app.application.use_cases.refund_sale import RefundSale
from app.infrastructure.api.dependencies.database_dependencies import get_uow_factory
from app.infrastructure.api.dto.request.quote_input import QuoteInput
from app.infrastructure.api.dto.request.refund_input import RefundInput
from app.infrastructure.api.dto.request.sale_input import SaleInput

router = APIRouter(prefix="/api/ventas")


@router.get("", tags=["Ventas"], response_model=None)
def sales(request: Request) -> list[SaleSummaryResponse]:
    return QuerySales(get_uow_factory(request)).execute()


@router.post("/cotizacion", tags=["Ventas"], response_model=None)
def quote(data: QuoteInput, request: Request) -> SaleQuoteResponse:
    return QuoteSale(get_uow_factory(request)).execute(data.to_command())


@router.post("", status_code=201, tags=["Ventas"], response_model=None)
def sale(data: SaleInput, request: Request) -> SaleDetailResponse:
    return CreateSale(get_uow_factory(request)).execute(data.to_command())


@router.get("/{id}", tags=["Ventas"], response_model=None)
def sale_detail(id: int, request: Request) -> SaleDetailResponse:
    return GetSale(get_uow_factory(request)).execute(id)


@router.post(
    "/{id}/devoluciones", status_code=201, tags=["Ventas"], response_model=None
)
def refund(id: int, data: RefundInput, request: Request) -> SaleDetailResponse:
    return RefundSale(get_uow_factory(request)).execute(id, data.to_command())
