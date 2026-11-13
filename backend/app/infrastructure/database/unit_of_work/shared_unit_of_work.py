from contextlib import AbstractContextManager
from types import TracebackType

from app.application.ports.i_unit_of_work import IUnitOfWork


class SharedUnitOfWork(AbstractContextManager[IUnitOfWork]):
    """La carga completa de la demo conserva la propiedad de la transacción."""

    def __init__(self, root: IUnitOfWork) -> None:
        self.root = root

    def __enter__(self) -> IUnitOfWork:
        return self.root

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        return False
