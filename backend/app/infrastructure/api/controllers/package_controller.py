from fastapi import APIRouter, Request

from app.application.dto.response.package_transition_response import (
    PackageTransitionResponse,
)
from app.application.use_cases.transition_package import TransitionPackage
from app.infrastructure.api.dependencies.database_dependencies import get_uow_factory
from app.infrastructure.api.dto.request.transition_input import TransitionInput

router = APIRouter(prefix="/api/bultos")


@router.post("/{id}/{accion}", tags=["Logística"], response_model=None)
def transition(
    id: int, accion: str, data: TransitionInput, request: Request
) -> PackageTransitionResponse:
    return TransitionPackage(get_uow_factory(request)).execute(
        id, accion, data.to_command()
    )
