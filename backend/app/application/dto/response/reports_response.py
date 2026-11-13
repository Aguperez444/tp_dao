from __future__ import annotations

from dataclasses import dataclass

from app.application.dto.response.report_data_response import ReportDataResponse


@dataclass(kw_only=True)
class ReportsResponse(ReportDataResponse):
    desde: str
    hasta: str
    establecimiento_id: int | None
