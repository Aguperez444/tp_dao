from app.domain.models.producto import Producto
from app.infrastructure.database.models.producto_orm import ProductoORM


class ProductoMapper:
    @staticmethod
    def orm_to_domain(instance: ProductoORM) -> Producto:
        return Producto(
            id=instance.id,
            nombre=instance.nombre,
            detalle=instance.detalle,
            categoria_id=instance.categoria_id,
            precio=instance.precio,
            costo_referencia=instance.costo_referencia,
            esta_activo=instance.esta_activo,
            codigo=instance.codigo,
        )

    @staticmethod
    def domain_to_orm(entity: Producto) -> ProductoORM:
        return ProductoORM(
            id=entity.id if entity.is_persisted() else None,
            nombre=entity.nombre,
            detalle=entity.detalle,
            categoria_id=entity.categoria_id,
            precio=entity.precio,
            costo_referencia=entity.costo_referencia,
            esta_activo=entity.esta_activo,
            codigo=entity.codigo,
        )
