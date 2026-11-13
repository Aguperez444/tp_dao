from app.application.dto.commands.city_command import CityCommand
from app.application.dto.response.ciudad_object_response import CiudadObjectResponse
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.catalog_validation_service import CatalogValidationService
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.models.ciudad import Ciudad


class SaveCiudad:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(self, data: CityCommand, id: int | None = None) -> CiudadObjectResponse:
        data = CatalogValidationService.normalize(data)
        with self.uow_factory(write=True) as uow:
            repository = uow.ciudad_repo
            CatalogValidationService.require_existing(repository, id)
            CatalogValidationService.unique_name(
                repository, data.nombre, id, provincia_id=data.provincia_id
            )
            EntityValidationService.require(uow.provincia_repo, data.provincia_id)
            entity = Ciudad(
                id=id or None, nombre=data.nombre, provincia_id=data.provincia_id
            )
            saved = CatalogValidationService.persist(repository, entity, id)
            return CiudadObjectResponse.from_entity(saved)
