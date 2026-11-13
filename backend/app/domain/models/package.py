from dataclasses import dataclass

from app.domain.services.shipping.package_state import PackageState


@dataclass
class Package:
    state: PackageState

    def execute(self, action: str) -> str:
        self.state = self.state.advance(action)
        return self.state.name
