from fastapi import APIRouter, Request

from app.application.dto.response.orden_reposicion_object_response import (
    OrdenReposicionObjectResponse,
)
from app.application.dto.response.remito_object_response import RemitoObjectResponse
from app.application.dto.response.replenishment_order_response import (
    ReplenishmentOrderResponse,
)
from app.application.use_cases.create_delivery import CreateDelivery
from app.application.use_cases.create_replenishment_order import (
    CreateReplenishmentOrder,
)
from app.application.use_cases.query_replenishment_orders import (
    QueryReplenishmentOrders,
)
from app.infrastructure.api.dependencies.database_dependencies import get_uow_factory
from app.infrastructure.api.dto.request.delivery_input import DeliveryInput
from app.infrastructure.api.dto.request.order_input import OrderInput

router = APIRouter(prefix="/api/reposiciones")


@router.get("", tags=["Logística"], response_model=None)
def orders(request: Request) -> list[ReplenishmentOrderResponse]:
    return QueryReplenishmentOrders(get_uow_factory(request)).execute()


@router.post("", status_code=201, tags=["Logística"], response_model=None)
def order(data: OrderInput, request: Request) -> OrdenReposicionObjectResponse:
    return CreateReplenishmentOrder(get_uow_factory(request)).execute(data.to_command())


@router.post("/{id}/remitos", status_code=201, tags=["Logística"], response_model=None)
def delivery(id: int, data: DeliveryInput, request: Request) -> RemitoObjectResponse:
    return CreateDelivery(get_uow_factory(request)).execute(id, data.numero_remito)
