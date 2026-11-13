from abc import ABC, abstractmethod

from app.application.dto.response.report_data_response import ReportDataResponse
from app.application.dto.response.stock_item_response import StockItemResponse
from app.application.dto.response.stock_movement_response import StockMovementResponse


class IReportsRepository(ABC):
    @abstractmethod
    def stock(self, local: int | None = None) -> list[StockItemResponse]:
        raise NotImplementedError

    @abstractmethod
    def movements(
        self, since: str, until: str, local: int | None = None
    ) -> list[StockMovementResponse]:
        raise NotImplementedError

    @abstractmethod
    def generate(
        self, since: str, until: str, local: int | None = None
    ) -> ReportDataResponse:
        raise NotImplementedError
