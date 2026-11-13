from fastapi import APIRouter, Request

from app.application.dto.response.health_response import HealthResponse
from app.application.dto.response.message_response import MessageResponse

router = APIRouter(prefix="/api")


@router.get("/salud", tags=["Sistema"], response_model=None)
def health() -> HealthResponse:
    return HealthResponse(estado="ok", version="2.0.0")


@router.post("/demo", status_code=201, tags=["Sistema"], response_model=None)
def demo(request: Request) -> MessageResponse:
    from app.infrastructure.database.seed_data import seed

    seed(request.app.state.database)
    return MessageResponse(mensaje="Datos de demostración cargados.")
