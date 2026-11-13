from dataclasses import replace

from app.application.dto.commands.product_command import ProductCommand
from app.application.dto.response.producto_object_response import ProductoObjectResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.catalog_validation_service import CatalogValidationService
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.producto import Producto
from app.domain.services.money_service import to_cents


class SaveProducto:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, data: ProductCommand, id: int | None = None
    ) -> ProductoObjectResponse:
        data = CatalogValidationService.normalize(data)
        with self.uow_factory(write=True) as uow:
            repository = uow.producto_repo
            CatalogValidationService.require_existing(repository, id)
            data = replace(data, codigo=data.codigo.upper())
            price = to_cents(data.precio)
            cost = to_cents(data.costo_referencia)
            if price <= 0:
                raise BusinessError("El precio de venta debe ser mayor que cero.")
            EntityValidationService.require(uow.categoria_repo, data.categoria_id)
            entity = Producto(
                id=id or None,
                nombre=data.nombre,
                detalle=data.detalle,
                categoria_id=data.categoria_id,
                precio=price,
                costo_referencia=cost,
                esta_activo=data.esta_activo,
                codigo=data.codigo,
            )
            saved = CatalogValidationService.persist(repository, entity, id)
            return ProductoObjectResponse.from_entity(saved)
