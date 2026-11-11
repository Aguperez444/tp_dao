from starlette.datastructures import Headers
from starlette.responses import JSONResponse

LOCAL_ORIGINS = ['http://127.0.0.1:5173','http://localhost:5173','http://127.0.0.1:4173','http://localhost:4173']


class LocalOriginMiddleware:
    """Rechaza escrituras desde páginas externas, incluso POST sin cuerpo."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http' and scope['method'] in ('POST','PUT','PATCH','DELETE'):
            origin = Headers(scope=scope).get('origin')
            if origin and origin not in LOCAL_ORIGINS:
                await JSONResponse({'detail':'Origen de la solicitud no permitido.'},status_code=403)(scope,receive,send)
                return
        await self.app(scope,receive,send)
