from app.domain.models.venta import Venta
from app.infrastructure.database.models.venta_orm import VentaORM


class VentaMapper:
    @staticmethod
    def orm_to_domain(instance: VentaORM) -> Venta:
        return Venta(
            id=instance.id,
            local_id=instance.local_id,
            metodo_pago_id=instance.metodo_pago_id,
            total=instance.total,
            fecha=instance.fecha,
            numero_comprobante=instance.numero_comprobante,
        )

    @staticmethod
    def domain_to_orm(entity: Venta) -> VentaORM:
        orm = VentaORM(
            local_id=entity.local_id,
            metodo_pago_id=entity.metodo_pago_id,
            total=entity.total,
            fecha=entity.fecha,
            numero_comprobante=entity.numero_comprobante,
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm