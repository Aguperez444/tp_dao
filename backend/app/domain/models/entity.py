class Entity:
    """Identidad de dominio, independiente de la sesión y del ORM."""

    def __init__(self, *, id: int | None = None) -> None:
        self._id = id

    @property
    def id(self) -> int:
        if self._id is None:
            raise ValueError("La entidad todavía no fue persistida.")
        return self._id

    def is_persisted(self) -> bool:
        return self._id is not None
