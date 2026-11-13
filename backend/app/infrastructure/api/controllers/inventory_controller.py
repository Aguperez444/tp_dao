from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, Request

from app.application.dto.response.existencia_object_response import (
    ExistenciaObjectResponse,
)
from app.application.dto.response.stock_item_response import StockItemResponse
from app.application.dto.response.stock_movement_response import StockMovementResponse
from app.application.use_cases.query_stock import QueryStock
from app.application.use_cases.query_stock_movements import QueryStockMovements
from app.application.use_cases.set_stock_minimum import SetStockMinimum
from app.infrastructure.api.dependencies.database_dependencies import (
    get_reports_repository,
    get_uow_factory,
)
from app.infrastructure.api.dto.request.minimum_input import MinimumInput

router = APIRouter(prefix="/api/inventario")


@router.get("", tags=["Inventario"], response_model=None)
def inventory(
    request: Request, establecimiento_id: Annotated[int | None, Query(gt=0)] = None
) -> list[StockItemResponse]:
    return QueryStock(get_reports_repository(request)).execute(establecimiento_id)


@router.put("/minimo", tags=["Inventario"], response_model=None)
def minimum(data: MinimumInput, request: Request) -> ExistenciaObjectResponse:
    return SetStockMinimum(get_uow_factory(request)).execute(
        data.establecimiento_id, data.producto_id, data.minimo_permitido
    )


@router.get("/movimientos", tags=["Inventario"], response_model=None)
def movements(
    request: Request,
    desde: date = date(2000, 1, 1),
    hasta: date | None = None,
    establecimiento_id: Annotated[int | None, Query(gt=0)] = None,
) -> list[StockMovementResponse]:
    return QueryStockMovements(get_reports_repository(request)).execute(
        desde, hasta or date.today(), establecimiento_id
    )
