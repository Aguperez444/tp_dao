from app.application.dto.commands.address_command import AddressCommand
from app.application.dto.response.domicilio_object_response import (
    DomicilioObjectResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.catalog_validation_service import CatalogValidationService
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.models.domicilio import Domicilio


class SaveDomicilio:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, data: AddressCommand, id: int | None = None
    ) -> DomicilioObjectResponse:
        data = CatalogValidationService.normalize(data)
        with self.uow_factory(write=True) as uow:
            repository = uow.domicilio_repo
            CatalogValidationService.require_existing(repository, id)
            EntityValidationService.require(uow.ciudad_repo, data.ciudad_id)
            entity = Domicilio(
                id=id or None,
                calle=data.calle,
                altura=data.altura,
                ciudad_id=data.ciudad_id,
            )
            saved = CatalogValidationService.persist(repository, entity, id)
            return DomicilioObjectResponse.from_entity(saved)
