from datetime import date

from app.application.dto.response.reports_response import ReportsResponse
from app.application.ports.i_reports_repository import IReportsRepository
from app.domain.services.report_period_service import ReportPeriodService


class GenerateReports:
    def __init__(self, repository: IReportsRepository) -> None:
        self.repository = repository

    def execute(
        self, since: date, until: date, local: int | None = None
    ) -> ReportsResponse:
        start, end = ReportPeriodService.range(since, until)
        report = self.repository.generate(start, end, local)
        return ReportsResponse(
            desde=since.isoformat(),
            hasta=until.isoformat(),
            establecimiento_id=local,
            ventas=report.ventas,
            productos=report.productos,
            existencias=report.existencias,
            rechazos=report.rechazos,
            transito=report.transito,
        )
