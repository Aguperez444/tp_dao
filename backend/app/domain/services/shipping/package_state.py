from abc import ABC, abstractmethod
from typing import NoReturn

from app.domain.exceptions.business_error import BusinessError


class PackageState(ABC):
    name: str

    def invalid(self) -> NoReturn:
        raise BusinessError(f"Operación no permitida para un bulto {self.name}.")

    @abstractmethod
    def advance(self, action: str) -> "PackageState":
        pass
