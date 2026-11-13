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
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory


class QueryCatalogs:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self) -> CatalogsResponse:
        with self.uow_factory() as uow:
            return CatalogsResponse(
                categoria=[
                    CategoriaObjectResponse.from_entity(entity)
                    for entity in uow.categoria_repo.list()
                ],
                ciudad=[
                    CiudadObjectResponse.from_entity(entity)
                    for entity in uow.ciudad_repo.list()
                ],
                domicilio=[
                    DomicilioObjectResponse.from_entity(entity)
                    for entity in uow.domicilio_repo.list()
                ],
                establecimiento=[
                    EstablecimientoObjectResponse.from_entity(entity)
                    for entity in uow.establecimiento_repo.list()
                ],
                estado_bulto=[
                    EstadoBultoObjectResponse.from_entity(entity)
                    for entity in uow.estado_bulto_repo.list()
                ],
                estado_compra=[
                    EstadoCompraObjectResponse.from_entity(entity)
                    for entity in uow.estado_compra_repo.list()
                ],
                estado_precinto=[
                    EstadoPrecintoObjectResponse.from_entity(entity)
                    for entity in uow.estado_precinto_repo.list()
                ],
                estado_remito=[
                    EstadoRemitoObjectResponse.from_entity(entity)
                    for entity in uow.estado_remito_repo.list()
                ],
                estado_reposicion=[
                    EstadoReposicionObjectResponse.from_entity(entity)
                    for entity in uow.estado_reposicion_repo.list()
                ],
                metodo_pago=[
                    MetodoPagoObjectResponse.from_entity(entity)
                    for entity in uow.metodo_pago_repo.list()
                ],
                motivo=[
                    MotivoObjectResponse.from_entity(entity)
                    for entity in uow.motivo_repo.list()
                ],
                producto=[
                    ProductoObjectResponse.from_entity(entity)
                    for entity in uow.producto_repo.list()
                ],
                proveedor=[
                    ProveedorObjectResponse.from_entity(entity)
                    for entity in uow.proveedor_repo.list()
                ],
                provincia=[
                    ProvinciaObjectResponse.from_entity(entity)
                    for entity in uow.provincia_repo.list()
                ],
            )
