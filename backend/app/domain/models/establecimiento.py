from app.domain.models.named_entity import NamedEntity


class Establecimiento(NamedEntity):
    def __init__(
        self,
        *,
        id: int | None = None,
        nombre: str,
        es_central: bool = False,
        domicilio_id: int,
    ) -> None:
        super().__init__(id=id, nombre=nombre)
        self.es_central: bool = es_central
        self.domicilio_id: int = domicilio_id
