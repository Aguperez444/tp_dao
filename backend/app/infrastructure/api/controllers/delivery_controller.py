from fastapi import APIRouter, Request

from app.application.dto.response.bulto_object_response import BultoObjectResponse
from app.application.use_cases.prepare_package import PreparePackage
from app.infrastructure.api.dependencies.database_dependencies import get_uow_factory
from app.infrastructure.api.dto.request.package_input import PackageInput

router = APIRouter(prefix="/api/remitos")


@router.post("/{id}/bultos", status_code=201, tags=["Logística"], response_model=None)
def package(id: int, data: PackageInput, request: Request) -> BultoObjectResponse:
    return PreparePackage(get_uow_factory(request)).execute(id, data.to_command())
