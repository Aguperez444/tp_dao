from app.domain.models.named_entity import NamedEntity


class Ciudad(NamedEntity):
    def __init__(
        self, *, id: int | None = None, nombre: str, provincia_id: int
    ) -> None:
        super().__init__(id=id, nombre=nombre)
        self.provincia_id: int = provincia_id
