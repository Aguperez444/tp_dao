from app.domain.models.entity import Entity


class Existencia(Entity):
    def __init__(
        self,
        *,
        id: int | None = None,
        establecimiento_id: int,
        producto_id: int,
        almacenado_total: int = 0,
        reservado: int = 0,
        minimo_permitido: int = 0,
    ) -> None:
        super().__init__(id=id)
        self.establecimiento_id: int = establecimiento_id
        self.producto_id: int = producto_id
        self.almacenado_total: int = almacenado_total
        self.reservado: int = reservado
        self.minimo_permitido: int = minimo_permitido
