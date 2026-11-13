from app.domain.models.detalle_compra import DetalleCompra
from app.infrastructure.database.models.detalle_compra_orm import DetalleCompraORM


class DetalleCompraMapper:
    @staticmethod
    def orm_to_domain(instance: DetalleCompraORM) -> DetalleCompra:
        return DetalleCompra(
            id=instance.id,
            producto_id=instance.producto_id,
            compra_id=instance.compra_id,
            cantidad=instance.cantidad,
            costo=instance.costo,
        )

    @staticmethod
    def domain_to_orm(entity: DetalleCompra) -> DetalleCompraORM:
        return DetalleCompraORM(
            id=entity.id if entity.is_persisted() else None,
            producto_id=entity.producto_id,
            compra_id=entity.compra_id,
            cantidad=entity.cantidad,
            costo=entity.costo,
        )
