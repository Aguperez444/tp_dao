from app.domain.models.entity import Entity


class DetalleVenta(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        producto_id: int,
        venta_id: int,
        cantidad: int,
        precio_unitario: int,
        descuento_aplicado: int,
        costo_unitario: int,
    ) -> None:
        super().__init__(id=id)
        self.producto_id: int = producto_id
        self.venta_id: int = venta_id
        self.cantidad: int = cantidad
        self.precio_unitario: int = precio_unitario
        self.descuento_aplicado: int = descuento_aplicado
        self.costo_unitario: int = costo_unitario
