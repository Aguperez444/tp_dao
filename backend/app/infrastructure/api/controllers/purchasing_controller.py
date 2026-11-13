from fastapi import APIRouter, Request

from app.application.dto.response.compra_object_response import CompraObjectResponse
from app.application.dto.response.purchase_summary_response import (
    PurchaseSummaryResponse,
)
from app.application.use_cases.create_purchase import CreatePurchase
from app.application.use_cases.query_purchases import QueryPurchases
from app.application.use_cases.receive_purchase import ReceivePurchase
from app.infrastructure.api.dependencies.database_dependencies import get_uow_factory
from app.infrastructure.api.dto.request.purchase_input import PurchaseInput

router = APIRouter(prefix="/api/compras")


@router.get("", tags=["Compras"], response_model=None)
def purchases(request: Request) -> list[PurchaseSummaryResponse]:
    return QueryPurchases(get_uow_factory(request)).execute()


@router.post("", status_code=201, tags=["Compras"], response_model=None)
def purchase(data: PurchaseInput, request: Request) -> CompraObjectResponse:
    return CreatePurchase(get_uow_factory(request)).execute(data.to_command())


@router.post("/{id}/recepcion", tags=["Compras"], response_model=None)
def receive_purchase(id: int, request: Request) -> CompraObjectResponse:
    return ReceivePurchase(get_uow_factory(request)).execute(id)
