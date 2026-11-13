from app.domain.models.entity import Entity


class DetalleReposicion(Entity):
    def __init__(
        self, *, id: int | None = None, producto_id: int, orden_id: int, cantidad: int
    ) -> None:
        super().__init__(id=id)
        self.producto_id: int = producto_id
        self.orden_id: int = orden_id
        self.cantidad: int = cantidad
