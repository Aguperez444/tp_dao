from contextlib import AbstractContextManager
from typing import Protocol

from app.application.ports.i_unit_of_work import IUnitOfWork


class IUnitOfWorkFactory(Protocol):
    def __call__(
        self, *, write: bool = False
    ) -> AbstractContextManager[IUnitOfWork]: ...
