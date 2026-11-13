from app.domain.models.named_entity import NamedEntity


class Proveedor(NamedEntity):
    def __init__(
        self, *, id: int | None = None, CUIT: str, nombre: str, esta_activo: bool = True
    ) -> None:
        super().__init__(id=id, nombre=nombre)
        self.CUIT: str = CUIT
        self.esta_activo: bool = esta_activo
