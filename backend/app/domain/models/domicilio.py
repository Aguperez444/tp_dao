from app.domain.models.entity import Entity


class Domicilio(Entity):
    def __init__(
        self, *, id: int | None = None, calle: str, altura: str, ciudad_id: int
    ) -> None:
        super().__init__(id=id)
        self.calle: str = calle
        self.altura: str = altura
        self.ciudad_id: int = ciudad_id
