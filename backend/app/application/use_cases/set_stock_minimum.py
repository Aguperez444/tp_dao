from app.application.dto.response.existencia_object_response import (
    ExistenciaObjectResponse,
)
from app.application.ports.i_unit_of_work_factory import IUnitOfWorkFactory
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.exceptions.business_error import BusinessError


class SetStockMinimum:
    def __init__(self, uow_factory: IUnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    def execute(
        self, local: int, product: int, minimum: int
    ) -> ExistenciaObjectResponse:
        if type(minimum) is not int or minimum < 0:
            raise BusinessError("El mínimo debe ser un entero no negativo.")
        with self.uow_factory(write=True) as uow:
            EntityValidationService.require(uow.establecimiento_repo, local)
            EntityValidationService.require(uow.producto_repo, product)
            stock = uow.existencia_repo.stock(local, product)
            stock.minimo_permitido = minimum
            return ExistenciaObjectResponse.from_entity(
                uow.existencia_repo.update(stock)
            )
