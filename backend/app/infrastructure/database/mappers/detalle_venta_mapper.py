from app.domain.models.detalle_venta import DetalleVenta
from app.infrastructure.database.models.detalle_venta_orm import DetalleVentaORM


class DetalleVentaMapper:
    @staticmethod
    def orm_to_domain(instance: DetalleVentaORM) -> DetalleVenta:
        return DetalleVenta(
            id=instance.id,
            producto_id=instance.producto_id,
            venta_id=instance.venta_id,
            cantidad=instance.cantidad,
            precio_unitario=instance.precio_unitario,
            descuento_aplicado=instance.descuento_aplicado,
            costo_unitario=instance.costo_unitario,
        )

    @staticmethod
    def domain_to_orm(entity: DetalleVenta) -> DetalleVentaORM:
        return DetalleVentaORM(
            id=entity.id if entity.is_persisted() else None,
            producto_id=entity.producto_id,
            venta_id=entity.venta_id,
            cantidad=entity.cantidad,
            precio_unitario=entity.precio_unitario,
            descuento_aplicado=entity.descuento_aplicado,
            costo_unitario=entity.costo_unitario,
        )
