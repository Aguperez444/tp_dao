from app.domain.models.entity import Entity


class Bulto(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        remito_id: int,
        estado_precinto_id: int,
        estado_bulto_id: int,
        codigo_precinto: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.remito_id: int = remito_id
        self.estado_precinto_id: int = estado_precinto_id
        self.estado_bulto_id: int = estado_bulto_id
        self.codigo_precinto: str | None = codigo_precinto
