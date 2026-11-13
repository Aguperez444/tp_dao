from app.domain.models.entity import Entity


class NamedEntity(Entity):
    def __init__(self, *, nombre: str, id: int | None = None) -> None:
        super().__init__(id=id)
        self.nombre = nombre
