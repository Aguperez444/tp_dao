from dataclasses import replace

from app.application.dto.commands.supplier_command import SupplierCommand
from app.application.dto.response.proveedor_object_response import (
    ProveedorObjectResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.catalog_validation_service import CatalogValidationService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.proveedor import Proveedor


class SaveProveedor:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, data: SupplierCommand, id: int | None = None
    ) -> ProveedorObjectResponse:
        data = CatalogValidationService.normalize(data)
        with self.uow_factory(write=True) as uow:
            repository = uow.proveedor_repo
            CatalogValidationService.require_existing(repository, id)
            data = replace(data, CUIT=data.CUIT.replace("-", "").replace(" ", ""))
            if (
                not data.CUIT.isascii()
                or not data.CUIT.isdigit()
                or len(data.CUIT) != 11
            ):
                raise BusinessError(
                    "El CUIT debe contener 11 dígitos (se admiten guiones)."
                )
            entity = Proveedor(
                id=id or None,
                CUIT=data.CUIT,
                nombre=data.nombre,
                esta_activo=data.esta_activo,
            )
            saved = CatalogValidationService.persist(repository, entity, id)
            return ProveedorObjectResponse.from_entity(saved)
