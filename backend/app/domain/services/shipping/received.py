from app.domain.services.shipping.package_state import PackageState


class Received(PackageState):
    name = "Recibido"

    def advance(self, action: str) -> PackageState:
        from app.domain.services.shipping.rejected import Rejected
        from app.domain.services.shipping.verified import Verified

        if action == "verificar":
            return Verified()
        if action == "rechazar":
            return Rejected()
        return self.invalid()
