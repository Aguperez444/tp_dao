from app.application.dto.response.stock_item_response import StockItemResponse
from app.application.ports.i_reports_repository import IReportsRepository


class QueryStock:
    def __init__(self, repository: IReportsRepository) -> None:
        self.repository = repository

    def execute(self, local: int | None = None) -> list[StockItemResponse]:
        return self.repository.stock(local)
