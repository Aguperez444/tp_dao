from starlette.datastructures import Headers
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.infrastructure.config.settings import LOCAL_ORIGINS


class LocalOriginMiddleware:
    """Rechaza escrituras desde páginas externas, incluso POST sin cuerpo."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["method"] in (
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ):
            origin = Headers(scope=scope).get("origin")
            if origin and origin not in LOCAL_ORIGINS:
                await JSONResponse(
                    {"detail": "Origen de la solicitud no permitido."}, status_code=403
                )(scope, receive, send)
                return
        await self.app(scope, receive, send)
