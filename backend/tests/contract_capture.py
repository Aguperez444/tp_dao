"""Escenario HTTP registrado antes de la refactorización, sobre una base temporal."""

import re
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import httpx
from app.infrastructure.start.main import create_app


def normalize(value):
    if isinstance(value, dict):
        return {
            key: ("<today>" if key == "hasta" else normalize(item))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}T.*", value):
        return "<timestamp>"
    return value


async def inline(function, *args, **kwargs):
    return function(*args, **kwargs)


async def capture():
    with TemporaryDirectory() as directory:
        app = create_app(Path(directory) / "contract.sqlite3")
        async with app.router.lifespan_context(app):
            with (
                patch("fastapi.routing.run_in_threadpool", inline),
                patch("starlette.routing.run_in_threadpool", inline),
            ):
                async with httpx.AsyncClient(
                    transport=httpx.ASGITransport(app=app), base_url="http://test"
                ) as client:
                    results = []

                    async def request(method, path, body=None):
                        response = await client.request(method, path, json=body)
                        results.append(
                            {
                                "method": method,
                                "path": path,
                                "status": response.status_code,
                                "body": normalize(response.json()),
                            }
                        )
                        return response

                    await request("POST", "/api/demo", {})
                    for path in (
                        "salud",
                        "catalogos",
                        "compras",
                        "reposiciones",
                        "ventas",
                        "ventas/1",
                        "inventario",
                        "inventario?establecimiento_id=2",
                        "inventario/movimientos",
                        "reportes",
                        "reportes?establecimiento_id=2",
                    ):
                        await request("GET", "/api/" + path)
                    await request("POST", "/api/demo", {})
                    await request("POST", "/api/compras/1/recepcion", {})
                    await request("GET", "/api/ventas/999")
                    await request(
                        "GET", "/api/reportes?desde=2026-12-01&hasta=2026-01-01"
                    )
                    await request(
                        "POST",
                        "/api/ventas/cotizacion",
                        {
                            "local_id": 2,
                            "politica": "descuento_10",
                            "detalles": [{"producto_id": 1, "cantidad": 2}],
                        },
                    )
                    await request(
                        "POST",
                        "/api/ventas",
                        {
                            "local_id": 2,
                            "metodo_pago_id": 1,
                            "politica": "descuento_10",
                            "importe_cobrado": "11700",
                            "detalles": [{"producto_id": 1, "cantidad": 2}],
                        },
                    )
                    await request(
                        "POST",
                        "/api/ventas/2/devoluciones",
                        {
                            "motivo_id": 1,
                            "metodo_reintegro_id": 1,
                            "detalle": "Devolución de prueba",
                            "productos_aptos": True,
                            "detalles": [{"producto_id": 1, "cantidad": 1}],
                        },
                    )
                    await request(
                        "PUT",
                        "/api/inventario/minimo",
                        {
                            "establecimiento_id": 2,
                            "producto_id": 1,
                            "minimo_permitido": 15,
                        },
                    )
                    for table, body in (
                        ("categoria", {"nombre": "Otra categoría"}),
                        ("provincia", {"nombre": "Santa Fe"}),
                        ("ciudad", {"nombre": "Rosario", "provincia_id": 2}),
                        (
                            "domicilio",
                            {"calle": "San Martín", "altura": "120", "ciudad_id": 2},
                        ),
                        ("establecimiento", {"nombre": "Local Sur", "domicilio_id": 4}),
                        (
                            "proveedor",
                            {"nombre": "Otro proveedor", "CUIT": "30-12345678-9"},
                        ),
                        (
                            "producto",
                            {
                                "codigo": "P-004",
                                "nombre": "Producto nuevo",
                                "categoria_id": 2,
                                "precio": "10.50",
                                "costo_referencia": "5.20",
                            },
                        ),
                        ("motivo", {"nombre": "Otro motivo"}),
                    ):
                        response = await request(
                            "POST", "/api/catalogos/" + table, body
                        )
                        assert response.status_code == 201, response.text
                        await request(
                            "PUT",
                            f"/api/catalogos/{table}/{response.json()['id']}",
                            body,
                        )
                    for path in (
                        "catalogos",
                        "inventario",
                        "ventas",
                        "ventas/2",
                        "reportes",
                        "inventario/movimientos",
                    ):
                        await request("GET", "/api/" + path)
                    with app.state.database.engine.connect() as connection:
                        schema = [
                            list(row)
                            for row in connection.exec_driver_sql(
                                "SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name"
                            )
                        ]
                    return {"requests": results, "database_schema": schema}
