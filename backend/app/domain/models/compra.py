from app.domain.models.entity import Entity


class Compra(Entity):
    def __init__(
        self, *, id: int | None = None, proveedor_id: int, estado_id: int, fecha: str
    ) -> None:
        super().__init__(id=id)
        self.proveedor_id: int = proveedor_id
        self.estado_id: int = estado_id
        self.fecha: str = fecha
