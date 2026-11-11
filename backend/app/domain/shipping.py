"""State: cada estado conoce sus acciones válidas y su sucesor."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from .errors import BusinessError


class PackageState(ABC):
    name: str

    def invalid(self):
        raise BusinessError(f'Operación no permitida para un bulto {self.name}.')

    @abstractmethod
    def advance(self, action: str) -> 'PackageState':
        pass


class Prepared(PackageState):
    name = 'Preparado'
    def advance(self, action):
        return Sealed() if action == 'precintar' else self.invalid()


class Sealed(PackageState):
    name = 'Precintado'
    def advance(self, action):
        return InTransit() if action == 'despachar' else self.invalid()


class InTransit(PackageState):
    name = 'En tránsito'
    def advance(self, action):
        return Received() if action == 'recibir' else self.invalid()


class Received(PackageState):
    name = 'Recibido'
    def advance(self, action):
        if action == 'verificar':
            return Verified()
        if action == 'rechazar':
            return Rejected()
        return self.invalid()


class Verified(PackageState):
    name = 'Verificado'
    def advance(self, action):
        return self.invalid()


class Rejected(PackageState):
    name = 'Rechazado'
    def advance(self, action):
        return self.invalid()


STATES = {state.name: state for state in (Prepared, Sealed, InTransit, Received, Verified, Rejected)}


@dataclass
class Package:
    state: PackageState

    def execute(self, action: str) -> str:
        self.state = self.state.advance(action)
        return self.state.name
