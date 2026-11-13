from app.domain.services.shipping.package_state import PackageState


class Rejected(PackageState):
    name = "Rechazado"

    def advance(self, action: str) -> PackageState:
        return self.invalid()
