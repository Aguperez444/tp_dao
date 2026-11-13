from dataclasses import fields, replace
from typing import TypeVar

from app.application.dto.commands.catalog_command import CatalogCommand
from app.application.ports.i_entity_repository import EntityT, IEntityRepository
from app.application.services.entity_validation_service import EntityValidationService
from app.domain.exceptions.business_error import BusinessError
from app.domain.models.ciudad import Ciudad
from app.domain.models.named_entity import NamedEntity

CommandT = TypeVar("CommandT", bound=CatalogCommand)
NamedT = TypeVar("NamedT", bound=NamedEntity)


class CatalogValidationService:
    @staticmethod
    def normalize(data: CommandT) -> CommandT:
        normalized: dict[str, str] = {}
        for field in fields(data):
            value = getattr(data, field.name)
            if isinstance(value, str):
                value = value.strip()
                if field.name != "detalle" and not value:
                    raise BusinessError("Complete los campos obligatorios.")
                normalized[field.name] = value
        return replace(data, **normalized)

    @staticmethod
    def require_existing(
        repository: IEntityRepository[EntityT], entity_id: int | None
    ) -> EntityT | None:
        return (
            EntityValidationService.require(repository, entity_id, active=False)
            if entity_id
            else None
        )

    @staticmethod
    def persist(
        repository: IEntityRepository[EntityT], entity: EntityT, entity_id: int | None
    ) -> EntityT:
        return repository.update(entity) if entity_id else repository.save(entity)

    @staticmethod
    def unique_name(
        repository: IEntityRepository[NamedT],
        name: str,
        entity_id: int | None,
        provincia_id: int | None = None,
    ) -> None:
        for other in repository.list():
            if other.id != entity_id and other.nombre.casefold() == name.casefold():
                if (
                    provincia_id is None
                    or isinstance(other, Ciudad)
                    and other.provincia_id == provincia_id
                ):
                    raise BusinessError("Ya existe un registro con ese nombre.")
