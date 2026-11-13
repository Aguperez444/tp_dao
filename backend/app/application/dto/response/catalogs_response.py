from __future__ import annotations

from dataclasses import dataclass

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
from app.application.dto.response.estado_bulto_object_response import (
    EstadoBultoObjectResponse,
)
from app.application.dto.response.estado_compra_object_response import (
    EstadoCompraObjectResponse,
)
from app.application.dto.response.estado_precinto_object_response import (
    EstadoPrecintoObjectResponse,
)
from app.application.dto.response.estado_remito_object_response import (
    EstadoRemitoObjectResponse,
)
from app.application.dto.response.estado_reposicion_object_response import (
    EstadoReposicionObjectResponse,
)
from app.application.dto.response.metodo_pago_object_response import (
    MetodoPagoObjectResponse,
)
from app.application.dto.response.motivo_object_response import MotivoObjectResponse
from app.application.dto.response.producto_object_response import ProductoObjectResponse
from app.application.dto.response.proveedor_object_response import (
    ProveedorObjectResponse,
)
from app.application.dto.response.provincia_object_response import (
    ProvinciaObjectResponse,
)


@dataclass(kw_only=True)
class CatalogsResponse:
    categoria: list[CategoriaObjectResponse]
    ciudad: list[CiudadObjectResponse]
    domicilio: list[DomicilioObjectResponse]
    establecimiento: list[EstablecimientoObjectResponse]
    estado_bulto: list[EstadoBultoObjectResponse]
    estado_compra: list[EstadoCompraObjectResponse]
    estado_precinto: list[EstadoPrecintoObjectResponse]
    estado_remito: list[EstadoRemitoObjectResponse]
    estado_reposicion: list[EstadoReposicionObjectResponse]
    metodo_pago: list[MetodoPagoObjectResponse]
    motivo: list[MotivoObjectResponse]
    producto: list[ProductoObjectResponse]
    proveedor: list[ProveedorObjectResponse]
    provincia: list[ProvinciaObjectResponse]
