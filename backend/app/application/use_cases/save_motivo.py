from app.application.dto.commands.named_command import NamedCommand
from app.application.dto.response.motivo_object_response import MotivoObjectResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.catalog_validation_service import CatalogValidationService
from app.domain.models.motivo import Motivo


class SaveMotivo:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, data: NamedCommand, id: int | None = None
    ) -> MotivoObjectResponse:
        data = CatalogValidationService.normalize(data)
        with self.uow_factory(write=True) as uow:
            repository = uow.motivo_repo
            CatalogValidationService.require_existing(repository, id)
            CatalogValidationService.unique_name(repository, data.nombre, id)
            entity = Motivo(id=id or None, nombre=data.nombre)
            saved = CatalogValidationService.persist(repository, entity, id)
            return MotivoObjectResponse.from_entity(saved)
