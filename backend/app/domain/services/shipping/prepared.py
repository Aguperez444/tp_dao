from app.domain.services.shipping.package_state import PackageState


class Prepared(PackageState):
    name = "Preparado"

    def advance(self, action: str) -> PackageState:
        from app.domain.services.shipping.sealed import Sealed

        return Sealed() if action == "precintar" else self.invalid()
