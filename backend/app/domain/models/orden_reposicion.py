from app.domain.models.entity import Entity


class OrdenReposicion(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        establecimiento_solicitante_id: int,
        establecimiento_proveedor_id: int,
        fecha: str,
        estado_id: int,
    ) -> None:
        super().__init__(id=id)
        self.establecimiento_solicitante_id: int = establecimiento_solicitante_id
        self.establecimiento_proveedor_id: int = establecimiento_proveedor_id
        self.fecha: str = fecha
        self.estado_id: int = estado_id
