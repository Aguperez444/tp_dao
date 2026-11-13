from app.domain.services.shipping.package_state import PackageState


class InTransit(PackageState):
    name = "En tránsito"

    def advance(self, action: str) -> PackageState:
        from app.domain.services.shipping.received import Received

        return Received() if action == "recibir" else self.invalid()
