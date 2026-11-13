from collections.abc import Sequence
from typing import TypeVar

from app.application.dto.commands.line_command import LineCommand
from app.application.ports.i_entity_repository import EntityT, IEntityRepository
from app.domain.exceptions.business_error import BusinessError
from app.domain.exceptions.not_found_error import NotFoundError
from app.domain.models.establecimiento import Establecimiento
from app.domain.models.named_entity import NamedEntity
from app.domain.models.producto import Producto

NamedT = TypeVar("NamedT", bound=NamedEntity)


class EntityValidationService:
    @staticmethod
    def require(
        repository: IEntityRepository[EntityT], entity_id: int, active: bool = True
    ) -> EntityT:
        entity = repository.get(entity_id)
        if entity is None:
            raise NotFoundError(f"No existe {repository.resource_name} #{entity_id}.")
        if active and getattr(entity, "esta_activo", None) is False:
            raise BusinessError(
                f"{repository.resource_name} #{entity_id} está inactivo."
            )
        return entity

    @staticmethod
    def state_id(repository: IEntityRepository[NamedT], name: str) -> int:
        entities = repository.list(nombre=name)
        if not entities:
            raise BusinessError(f"Estado o referencia no configurado: {name}.")
        return entities[0].id

    @staticmethod
    def state_name(repository: IEntityRepository[NamedT], entity_id: int) -> str:
        return EntityValidationService.require(repository, entity_id).nombre

    @staticmethod
    def local(
        repository: IEntityRepository[Establecimiento],
        entity_id: int,
        central: bool = False,
    ) -> Establecimiento:
        establishment = EntityValidationService.require(repository, entity_id)
        if establishment.es_central != central:
            raise BusinessError(
                "Se requiere un centro de distribución."
                if central
                else "Se requiere un local de venta."
            )
        return establishment

    @staticmethod
    def central(repository: IEntityRepository[Establecimiento]) -> Establecimiento:
        establishments = repository.list(es_central=True)
        if len(establishments) != 1:
            raise BusinessError("Registre primero el único centro de distribución.")
        return establishments[0]

    @staticmethod
    def lines(
        repository: IEntityRepository[Producto], lines: Sequence[LineCommand]
    ) -> dict[int, int]:
        if not lines:
            raise BusinessError("La operación debe contener productos.")
        quantities: dict[int, int] = {}
        for line in lines:
            if type(line.cantidad) is not int or line.cantidad <= 0:
                raise BusinessError("Las cantidades deben ser enteros positivos.")
            EntityValidationService.require(repository, line.producto_id)
            if line.producto_id in quantities:
                raise BusinessError(
                    "Incluya cada producto una sola vez, consolidando sus cantidades."
                )
            quantities[line.producto_id] = line.cantidad
        return quantities
