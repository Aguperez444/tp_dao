from app.domain.models.entity import Entity


class CambioEstadoBulto(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        bulto_id: int,
        estado_bulto_id: int,
        fecha: str,
        responsable: str,
        observacion: str,
    ) -> None:
        super().__init__(id=id)
        self.bulto_id: int = bulto_id
        self.estado_bulto_id: int = estado_bulto_id
        self.fecha: str = fecha
        self.responsable: str = responsable
        self.observacion: str = observacion
