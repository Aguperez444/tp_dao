from app.domain.models.named_entity import NamedEntity


class Producto(NamedEntity):
    def __init__(
        self,
        *,
        id: int | None = None,
        nombre: str,
        detalle: str = "",
        categoria_id: int,
        precio: int,
        costo_referencia: int,
        esta_activo: bool = True,
        codigo: str,
    ) -> None:
        super().__init__(id=id, nombre=nombre)
        self.detalle: str = detalle
        self.categoria_id: int = categoria_id
        self.precio: int = precio
        self.costo_referencia: int = costo_referencia
        self.esta_activo: bool = esta_activo
        self.codigo: str = codigo
