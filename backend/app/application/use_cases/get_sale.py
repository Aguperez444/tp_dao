from __future__ import annotations

from app.application.dto.response.sale_detail_response import SaleDetailResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.sale_detail_service import SaleDetailService


class GetSale:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, id: int) -> SaleDetailResponse:
        with self.uow_factory() as uow:
            return SaleDetailService.get(uow, id)
