from app.application.dto.commands.named_command import NamedCommand
from app.application.dto.response.provincia_object_response import (
    ProvinciaObjectResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.catalog_validation_service import CatalogValidationService
from app.domain.models.provincia import Provincia


class SaveProvincia:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, data: NamedCommand, id: int | None = None
    ) -> ProvinciaObjectResponse:
        data = CatalogValidationService.normalize(data)
        with self.uow_factory(write=True) as uow:
            repository = uow.provincia_repo
            CatalogValidationService.require_existing(repository, id)
            CatalogValidationService.unique_name(repository, data.nombre, id)
            entity = Provincia(id=id or None, nombre=data.nombre)
            saved = CatalogValidationService.persist(repository, entity, id)
            return ProvinciaObjectResponse.from_entity(saved)
