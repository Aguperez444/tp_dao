from app.domain.models.metodo_pago import MetodoPago
from app.infrastructure.database.models.metodo_pago_orm import MetodoPagoORM


class MetodoPagoMapper:
    @staticmethod
    def orm_to_domain(instance: MetodoPagoORM) -> MetodoPago:
        return MetodoPago(id=instance.id, nombre=instance.nombre)

    @staticmethod
    def domain_to_orm(entity: MetodoPago) -> MetodoPagoORM:
        return MetodoPagoORM(
            id=entity.id if entity.is_persisted() else None, nombre=entity.nombre
        )
