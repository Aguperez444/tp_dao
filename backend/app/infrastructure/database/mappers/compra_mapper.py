from app.domain.models.compra import Compra
from app.infrastructure.database.models.compra_orm import CompraORM


class CompraMapper:
    @staticmethod
    def orm_to_domain(instance: CompraORM) -> Compra:
        return Compra(
            id=instance.id,
            proveedor_id=instance.proveedor_id,
            estado_id=instance.estado_id,
            fecha=instance.fecha,
        )

    @staticmethod
    def domain_to_orm(entity: Compra) -> CompraORM:
        return CompraORM(
            id=entity.id if entity.is_persisted() else None,
            proveedor_id=entity.proveedor_id,
            estado_id=entity.estado_id,
            fecha=entity.fecha,
        )
