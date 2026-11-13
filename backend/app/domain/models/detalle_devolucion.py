from app.domain.models.entity import Entity


class DetalleDevolucion(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        producto_id: int,
        devolucion_id: int,
        cantidad: int,
        importe_unitario: int,
    ) -> None:
        super().__init__(id=id)
        self.producto_id: int = producto_id
        self.devolucion_id: int = devolucion_id
        self.cantidad: int = cantidad
        self.importe_unitario: int = importe_unitario
