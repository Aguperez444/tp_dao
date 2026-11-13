from datetime import date

from app.application.dto.response.stock_movement_response import StockMovementResponse
from app.application.ports.i_reports_repository import IReportsRepository
from app.domain.services.report_period_service import ReportPeriodService


class QueryStockMovements:
    def __init__(self, repository: IReportsRepository) -> None:
        self.repository = repository

    def execute(
        self, since: date, until: date, local: int | None = None
    ) -> list[StockMovementResponse]:
        start, end = ReportPeriodService.range(since, until)
        return self.repository.movements(start, end, local)
