from app.domain.models.estado_compra import EstadoCompra
from app.infrastructure.database.models.estado_compra_orm import EstadoCompraORM


class EstadoCompraMapper:
    @staticmethod
    def orm_to_domain(instance: EstadoCompraORM) -> EstadoCompra:
        return EstadoCompra(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: EstadoCompra) -> EstadoCompraORM:
        orm = EstadoCompraORM(
            nombre=entity.nombre
        )
        if entity.is_persisted():
            orm.id = entity.id
        return orm
