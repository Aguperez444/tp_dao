import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError

from app.domain.exceptions.business_error import BusinessError
from app.domain.exceptions.not_found_error import NotFoundError
from app.infrastructure.api.controllers import (
    catalog_controller,
    delivery_controller,
    inventory_controller,
    package_controller,
    purchasing_controller,
    replenishment_controller,
    reporting_controller,
    sales_controller,
    system_controller,
)
from app.infrastructure.api.middleware.local_origin_middleware import (
    LocalOriginMiddleware,
)
from app.infrastructure.config.settings import DEFAULT_DB, LOCAL_ORIGINS
from app.infrastructure.database.database import Database


def create_app(db_path: str | Path | None = None) -> FastAPI:
    database = Database(db_path or os.environ.get("NEXO_DB_PATH", DEFAULT_DB))

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        database.initialize()
        yield
        database.dispose()

    app = FastAPI(
        title="Nexo · Distribución y ventas",
        version="2.0.0",
        description="TP integrador DAO, grupo 40. Importes de respuesta en centavos; importes de entrada en pesos. Comprobantes internos académicos.",
        lifespan=lifespan,
    )
    app.state.database = database
    app.add_middleware(
        CORSMiddleware,
        allow_origins=LOCAL_ORIGINS,
        allow_methods=["GET", "POST", "PUT"],
        allow_headers=["Content-Type"],
    )
    app.add_middleware(LocalOriginMiddleware)

    @app.exception_handler(BusinessError)
    async def business_error(request: Request, exc: BusinessError) -> JSONResponse:
        return JSONResponse(
            status_code=404 if isinstance(exc, NotFoundError) else 409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Identificador duplicado o relación inválida. No se guardó la operación."
            },
        )

    @app.exception_handler(OperationalError)
    async def operational_error(
        request: Request, exc: OperationalError
    ) -> JSONResponse:
        if "locked" not in str(exc).lower() and "busy" not in str(exc).lower():
            raise exc
        return JSONResponse(
            status_code=503,
            content={"detail": "La base de datos está ocupada. Intente nuevamente."},
        )

    app.include_router(catalog_controller.router)
    app.include_router(purchasing_controller.router)
    app.include_router(replenishment_controller.router)
    app.include_router(delivery_controller.router)
    app.include_router(package_controller.router)
    app.include_router(sales_controller.router)
    app.include_router(inventory_controller.router)
    app.include_router(reporting_controller.router)
    app.include_router(system_controller.router)
    return app


app = create_app()
