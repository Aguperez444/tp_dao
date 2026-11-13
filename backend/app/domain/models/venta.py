from app.domain.models.entity import Entity


class Venta(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        local_id: int,
        metodo_pago_id: int,
        total: int,
        fecha: str,
        numero_comprobante: str,
    ) -> None:
        super().__init__(id=id)
        self.local_id: int = local_id
        self.metodo_pago_id: int = metodo_pago_id
        self.total: int = total
        self.fecha: str = fecha
        self.numero_comprobante: str = numero_comprobante
