from app.domain.models.named_entity import NamedEntity


class EstadoRemito(NamedEntity):
    def __init__(self, *, id: int | None = None, nombre: str) -> None:
        super().__init__(id=id, nombre=nombre)
