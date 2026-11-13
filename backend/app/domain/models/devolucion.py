from app.domain.models.entity import Entity


class Devolucion(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        venta_id: int,
        motivo_id: int,
        metodo_reintegro_id: int,
        detalle: str,
        fecha: str,
    ) -> None:
        super().__init__(id=id)
        self.venta_id: int = venta_id
        self.motivo_id: int = motivo_id
        self.metodo_reintegro_id: int = metodo_reintegro_id
        self.detalle: str = detalle
        self.fecha: str = fecha
