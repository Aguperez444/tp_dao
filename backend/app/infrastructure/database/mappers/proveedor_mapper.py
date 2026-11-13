from app.domain.models.proveedor import Proveedor
from app.infrastructure.database.models.proveedor_orm import ProveedorORM


class ProveedorMapper:
    @staticmethod
    def orm_to_domain(instance: ProveedorORM) -> Proveedor:
        return Proveedor(
            id=instance.id,
            CUIT=instance.CUIT,
            nombre=instance.nombre,
            esta_activo=instance.esta_activo,
        )

    @staticmethod
    def domain_to_orm(entity: Proveedor) -> ProveedorORM:
        return ProveedorORM(
            id=entity.id if entity.is_persisted() else None,
            CUIT=entity.CUIT,
            nombre=entity.nombre,
            esta_activo=entity.esta_activo,
        )
