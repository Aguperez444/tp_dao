from app.domain.models.entity import Entity


class DetalleCompra(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        producto_id: int,
        compra_id: int,
        cantidad: int,
        costo: int,
    ) -> None:
        super().__init__(id=id)
        self.producto_id: int = producto_id
        self.compra_id: int = compra_id
        self.cantidad: int = cantidad
        self.costo: int = costo
