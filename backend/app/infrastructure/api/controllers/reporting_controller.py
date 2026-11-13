from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, Request

from app.application.dto.response.reports_response import ReportsResponse
from app.application.use_cases.generate_reports import GenerateReports
from app.infrastructure.api.dependencies.database_dependencies import (
    get_reports_repository,
)

router = APIRouter(prefix="/api/reportes")


@router.get("", tags=["Reportes"], response_model=None)
def reports(
    request: Request,
    desde: date = date(2000, 1, 1),
    hasta: date | None = None,
    establecimiento_id: Annotated[int | None, Query(gt=0)] = None,
) -> ReportsResponse:
    return GenerateReports(get_reports_repository(request)).execute(
        desde, hasta or date.today(), establecimiento_id
    )
