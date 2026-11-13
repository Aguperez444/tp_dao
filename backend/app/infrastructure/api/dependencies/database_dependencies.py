from fastapi import Request

from app.application.ports.i_reports_repository import IReportsRepository
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.infrastructure.database.repositories.reports_repository_impl import (
    ReportsRepositoryImpl,
)


def get_uow_factory(request: Request) -> IUnitOfWorkFactory:
    return request.app.state.database.uow


def get_reports_repository(request: Request) -> IReportsRepository:
    return ReportsRepositoryImpl(request.app.state.database)
