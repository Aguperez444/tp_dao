from fastapi import APIRouter, Request

from app.application.dto.response.catalogs_response import CatalogsResponse
from app.application.dto.response.categoria_object_response import (
    CategoriaObjectResponse,
)
from app.application.dto.response.ciudad_object_response import CiudadObjectResponse
from app.application.dto.response.domicilio_object_response import (
    DomicilioObjectResponse,
)
from app.application.dto.response.establecimiento_object_response import (
    EstablecimientoObjectResponse,
)
from app.application.dto.response.motivo_object_response import MotivoObjectResponse
from app.application.dto.response.producto_object_response import ProductoObjectResponse
from app.application.dto.response.proveedor_object_response import (
    ProveedorObjectResponse,
)
from app.application.dto.response.provincia_object_response import (
    ProvinciaObjectResponse,
)
from app.application.use_cases.query_catalogs import QueryCatalogs
from app.application.use_cases.save_categoria import SaveCategoria
from app.application.use_cases.save_ciudad import SaveCiudad
from app.application.use_cases.save_domicilio import SaveDomicilio
from app.application.use_cases.save_establecimiento import SaveEstablecimiento
from app.application.use_cases.save_motivo import SaveMotivo
from app.application.use_cases.save_producto import SaveProducto
from app.application.use_cases.save_proveedor import SaveProveedor
from app.application.use_cases.save_provincia import SaveProvincia
from app.infrastructure.api.dependencies.database_dependencies import get_uow_factory
from app.infrastructure.api.dto.request.address_input import AddressInput
from app.infrastructure.api.dto.request.city_input import CityInput
from app.infrastructure.api.dto.request.establishment_input import EstablishmentInput
from app.infrastructure.api.dto.request.named_input import NamedInput
from app.infrastructure.api.dto.request.product_input import ProductInput
from app.infrastructure.api.dto.request.supplier_input import SupplierInput

router = APIRouter(prefix="/api/catalogos")


@router.post("/categoria", status_code=201, tags=["Catálogos"], response_model=None)
def crear_categoria(data: NamedInput, request: Request) -> CategoriaObjectResponse:
    return SaveCategoria(get_uow_factory(request)).execute(data.to_command())


@router.put("/categoria/{id}", tags=["Catálogos"], response_model=None)
def editar_categoria(
    id: int, data: NamedInput, request: Request
) -> CategoriaObjectResponse:
    return SaveCategoria(get_uow_factory(request)).execute(data.to_command(), id)


@router.post("/provincia", status_code=201, tags=["Catálogos"], response_model=None)
def crear_provincia(data: NamedInput, request: Request) -> ProvinciaObjectResponse:
    return SaveProvincia(get_uow_factory(request)).execute(data.to_command())


@router.put("/provincia/{id}", tags=["Catálogos"], response_model=None)
def editar_provincia(
    id: int, data: NamedInput, request: Request
) -> ProvinciaObjectResponse:
    return SaveProvincia(get_uow_factory(request)).execute(data.to_command(), id)


@router.post("/ciudad", status_code=201, tags=["Catálogos"], response_model=None)
def crear_ciudad(data: CityInput, request: Request) -> CiudadObjectResponse:
    return SaveCiudad(get_uow_factory(request)).execute(data.to_command())


@router.put("/ciudad/{id}", tags=["Catálogos"], response_model=None)
def editar_ciudad(id: int, data: CityInput, request: Request) -> CiudadObjectResponse:
    return SaveCiudad(get_uow_factory(request)).execute(data.to_command(), id)


@router.post("/domicilio", status_code=201, tags=["Catálogos"], response_model=None)
def crear_domicilio(data: AddressInput, request: Request) -> DomicilioObjectResponse:
    return SaveDomicilio(get_uow_factory(request)).execute(data.to_command())


@router.put("/domicilio/{id}", tags=["Catálogos"], response_model=None)
def editar_domicilio(
    id: int, data: AddressInput, request: Request
) -> DomicilioObjectResponse:
    return SaveDomicilio(get_uow_factory(request)).execute(data.to_command(), id)


@router.post(
    "/establecimiento", status_code=201, tags=["Catálogos"], response_model=None
)
def crear_establecimiento(
    data: EstablishmentInput, request: Request
) -> EstablecimientoObjectResponse:
    return SaveEstablecimiento(get_uow_factory(request)).execute(data.to_command())


@router.put("/establecimiento/{id}", tags=["Catálogos"], response_model=None)
def editar_establecimiento(
    id: int, data: EstablishmentInput, request: Request
) -> EstablecimientoObjectResponse:
    return SaveEstablecimiento(get_uow_factory(request)).execute(data.to_command(), id)


@router.post("/proveedor", status_code=201, tags=["Catálogos"], response_model=None)
def crear_proveedor(data: SupplierInput, request: Request) -> ProveedorObjectResponse:
    return SaveProveedor(get_uow_factory(request)).execute(data.to_command())


@router.put("/proveedor/{id}", tags=["Catálogos"], response_model=None)
def editar_proveedor(
    id: int, data: SupplierInput, request: Request
) -> ProveedorObjectResponse:
    return SaveProveedor(get_uow_factory(request)).execute(data.to_command(), id)


@router.post("/producto", status_code=201, tags=["Catálogos"], response_model=None)
def crear_producto(data: ProductInput, request: Request) -> ProductoObjectResponse:
    return SaveProducto(get_uow_factory(request)).execute(data.to_command())


@router.put("/producto/{id}", tags=["Catálogos"], response_model=None)
def editar_producto(
    id: int, data: ProductInput, request: Request
) -> ProductoObjectResponse:
    return SaveProducto(get_uow_factory(request)).execute(data.to_command(), id)


@router.post("/motivo", status_code=201, tags=["Catálogos"], response_model=None)
def crear_motivo(data: NamedInput, request: Request) -> MotivoObjectResponse:
    return SaveMotivo(get_uow_factory(request)).execute(data.to_command())


@router.put("/motivo/{id}", tags=["Catálogos"], response_model=None)
def editar_motivo(id: int, data: NamedInput, request: Request) -> MotivoObjectResponse:
    return SaveMotivo(get_uow_factory(request)).execute(data.to_command(), id)


@router.get("", tags=["Catálogos"], response_model=None)
def catalogs(request: Request) -> CatalogsResponse:
    return QueryCatalogs(get_uow_factory(request)).execute()
