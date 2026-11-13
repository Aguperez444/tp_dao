from app.domain.models.entity import Entity


class DetalleBulto(Entity):
    def __init__(
        self, *, id: int | None = None, producto_id: int, bulto_id: int, cantidad: int
    ) -> None:
        super().__init__(id=id)
        self.producto_id: int = producto_id
        self.bulto_id: int = bulto_id
        self.cantidad: int = cantidad
