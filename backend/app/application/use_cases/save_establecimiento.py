from app.application.dto.commands.establishment_command import EstablishmentCommand
from app.application.dto.response.establecimiento_object_response import (
    EstablecimientoObjectResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.catalog_validation_service import CatalogValidationService
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.establecimiento import Establecimiento


class SaveEstablecimiento:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, data: EstablishmentCommand, id: int | None = None
    ) -> EstablecimientoObjectResponse:
        data = CatalogValidationService.normalize(data)
        with self.uow_factory(write=True) as uow:
            repository = uow.establecimiento_repo
            previous = (
                EntityValidationService.require(repository, id, active=False)
                if id
                else None
            )
            CatalogValidationService.unique_name(repository, data.nombre, id)
            EntityValidationService.require(uow.domicilio_repo, data.domicilio_id)
            if previous and previous.es_central != data.es_central:
                raise BusinessError(
                    "No se puede convertir un local en CD ni un CD en local."
                )
            if data.es_central and any(
                (other.id != id for other in repository.list(es_central=True))
            ):
                raise BusinessError("Solo puede existir un centro de distribución.")
            entity = Establecimiento(
                id=id or None,
                nombre=data.nombre,
                es_central=data.es_central,
                domicilio_id=data.domicilio_id,
            )
            saved = CatalogValidationService.persist(repository, entity, id)
            return EstablecimientoObjectResponse.from_entity(saved)
