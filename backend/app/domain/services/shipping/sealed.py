from app.domain.services.shipping.package_state import PackageState


class Sealed(PackageState):
    name = "Precintado"

    def advance(self, action: str) -> PackageState:
        from app.domain.services.shipping.in_transit import InTransit

        return InTransit() if action == "despachar" else self.invalid()
