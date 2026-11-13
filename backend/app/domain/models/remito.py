from app.domain.models.entity import Entity


class Remito(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        orden_reposicion_id: int,
        estado_remito_id: int,
        numero_remito: str,
        fecha_emision: str,
    ) -> None:
        super().__init__(id=id)
        self.orden_reposicion_id: int = orden_reposicion_id
        self.estado_remito_id: int = estado_remito_id
        self.numero_remito: str = numero_remito
        self.fecha_emision: str = fecha_emision
