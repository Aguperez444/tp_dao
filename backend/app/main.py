from contextlib import asynccontextmanager
from pathlib import Path
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from app.api.routes import router
from app.api.middleware import LocalOriginMiddleware, LOCAL_ORIGINS
from app.application.catalog import CatalogService
from app.application.purchasing import PurchasingService
from app.application.logistics import LogisticsService
from app.application.sales import SalesService
from app.application.reporting import ReportingService
from app.domain.errors import BusinessError, NotFoundError
from app.infrastructure.database import Database
from app.infrastructure.reports import ReportsRepository

DEFAULT_DB = Path(__file__).resolve().parents[1] / 'data' / 'nexo.sqlite3'


def create_app(db_path=None):
    database = Database(db_path or os.environ.get('NEXO_DB_PATH',DEFAULT_DB))
    @asynccontextmanager
    async def lifespan(app):
        database.initialize()
        yield
        database.dispose()
    app = FastAPI(title='Nexo · Distribución y ventas',version='2.0.0',description='TP integrador DAO, grupo 40. Importes de respuesta en centavos; importes de entrada en pesos. Comprobantes internos académicos.',lifespan=lifespan)
    app.state.database = database
    app.state.catalog = CatalogService(database.uow)
    app.state.purchasing = PurchasingService(database.uow)
    app.state.logistics = LogisticsService(database.uow)
    app.state.sales = SalesService(database.uow)
    app.state.reporting = ReportingService(ReportsRepository(database))
    app.add_middleware(CORSMiddleware,allow_origins=LOCAL_ORIGINS,allow_methods=['GET','POST','PUT'],allow_headers=['Content-Type'])
    app.add_middleware(LocalOriginMiddleware)
    @app.exception_handler(BusinessError)
    async def business_error(request: Request,exc: BusinessError):
        return JSONResponse(status_code=404 if isinstance(exc,NotFoundError) else 409,content={'detail':str(exc)})
    @app.exception_handler(IntegrityError)
    async def integrity_error(request: Request,exc: IntegrityError):
        return JSONResponse(status_code=409,content={'detail':'Identificador duplicado o relación inválida. No se guardó la operación.'})
    @app.exception_handler(OperationalError)
    async def operational_error(request: Request,exc: OperationalError):
        if 'locked' not in str(exc).lower() and 'busy' not in str(exc).lower():
            raise exc
        return JSONResponse(status_code=503,content={'detail':'La base de datos está ocupada. Intente nuevamente.'})
    app.include_router(router)
    return app


app = create_app()
