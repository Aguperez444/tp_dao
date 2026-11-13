from app.infrastructure.database.models.estado_bulto_orm import EstadoBultoORM
from app.infrastructure.database.models.estado_compra_orm import EstadoCompraORM
from app.infrastructure.database.models.estado_precinto_orm import EstadoPrecintoORM
from app.infrastructure.database.models.estado_remito_orm import EstadoRemitoORM
from app.infrastructure.database.models.estado_reposicion_orm import EstadoReposicionORM
from app.infrastructure.database.models.metodo_pago_orm import MetodoPagoORM
from app.infrastructure.database.models.motivo_orm import MotivoORM

LOOKUPS = {
    EstadoCompraORM: ("Pendiente", "Recibida"),
    EstadoReposicionORM: (
        "Pendiente",
        "En preparación",
        "En tránsito",
        "Completada",
        "Con rechazos",
    ),
    EstadoRemitoORM: (
        "Pendiente",
        "En tránsito",
        "Recibido",
        "Verificado",
        "Rechazado",
    ),
    EstadoPrecintoORM: ("Sin colocar", "Intacto", "Violado", "No coincide"),
    EstadoBultoORM: (
        "Preparado",
        "Precintado",
        "En tránsito",
        "Recibido",
        "Verificado",
        "Rechazado",
    ),
    MetodoPagoORM: ("Efectivo", "Tarjeta", "Transferencia"),
    MotivoORM: ("Cambio solicitado", "Error en la compra", "Disconformidad"),
}
