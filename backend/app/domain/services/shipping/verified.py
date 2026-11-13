from app.domain.services.shipping.package_state import PackageState


class Verified(PackageState):
    name = "Verificado"

    def advance(self, action: str) -> PackageState:
        return self.invalid()
