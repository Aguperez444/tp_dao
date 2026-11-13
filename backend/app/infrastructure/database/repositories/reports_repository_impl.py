from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import text

from app.application.dto.response.product_ranking_response import ProductRankingResponse
from app.application.dto.response.rejected_package_response import (
    RejectedPackageResponse,
)
from app.application.dto.response.report_data_response import ReportDataResponse
from app.application.dto.response.sales_by_payment_response import (
    SalesByPaymentResponse,
)
from app.application.dto.response.stock_item_response import StockItemResponse
from app.application.dto.response.stock_movement_response import StockMovementResponse
from app.application.dto.response.transit_summary_response import TransitSummaryResponse
from app.application.ports.i_reports_repository import IReportsRepository

if TYPE_CHECKING:
    from app.infrastructure.database.database import Database
ResultT = TypeVar("ResultT")


class ReportsRepositoryImpl(IReportsRepository):
    def __init__(self, database: Database) -> None:
        self.database = database

    def query(
        self,
        sql: str,
        parameters: dict[str, str | int | None],
        response_type: Callable[..., ResultT],
    ) -> list[ResultT]:
        with self.database.engine.connect() as connection:
            return [
                response_type(**row)
                for row in connection.execute(text(sql), parameters).mappings()
            ]

    def stock(self, local: int | None = None) -> list[StockItemResponse]:
        return self.query(
            "SELECT e.id establecimiento_id,e.nombre establecimiento,p.id producto_id,p.codigo,p.nombre producto,\n          COALESCE(x.almacenado_total,0) almacenado_total,COALESCE(x.reservado,0) reservado,\n          COALESCE(x.almacenado_total-x.reservado,0) disponible,COALESCE(x.minimo_permitido,0) minimo_permitido,\n          MAX(0,COALESCE(x.minimo_permitido-x.almacenado_total+x.reservado,0)) faltante,\n          COALESCE(x.almacenado_total,0)*p.costo_referencia valorizacion\n          FROM establecimiento e CROSS JOIN producto p LEFT JOIN existencia x ON x.establecimiento_id=e.id AND x.producto_id=p.id\n          WHERE (:local IS NULL OR e.id=:local) ORDER BY faltante DESC,e.nombre,p.nombre",
            {"local": local},
            StockItemResponse,
        )

    def movements(
        self, since: str, until: str, local: int | None = None
    ) -> list[StockMovementResponse]:
        return self.query(
            "WITH movimientos AS (\n          SELECT c.fecha,e.id establecimiento_id,l.producto_id,l.cantidad,'Compra recibida' concepto,'C-'||c.id referencia\n          FROM compra c JOIN estado_compra ec ON ec.id=c.estado_id JOIN detalle_compra l ON l.compra_id=c.id CROSS JOIN establecimiento e\n          WHERE ec.nombre='Recibida' AND e.es_central=1\n          UNION ALL SELECT ev.fecha,o.establecimiento_proveedor_id,l.producto_id,-l.cantidad,'Despacho','B-'||b.id\n          FROM cambio_estado_bulto ev JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id JOIN bulto b ON b.id=ev.bulto_id\n          JOIN remito r ON r.id=b.remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id JOIN detalle_bulto l ON l.bulto_id=b.id WHERE eb.nombre='En tránsito'\n          UNION ALL SELECT ultimo.fecha,o.establecimiento_solicitante_id,l.producto_id,l.cantidad,'Recepción verificada',r.numero_remito\n          FROM remito r JOIN estado_remito er ON er.id=r.estado_remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id\n          JOIN bulto b ON b.remito_id=r.id JOIN detalle_bulto l ON l.bulto_id=b.id\n          JOIN (SELECT b2.remito_id,MAX(ev.fecha) fecha FROM cambio_estado_bulto ev JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id JOIN bulto b2 ON b2.id=ev.bulto_id WHERE eb.nombre='Verificado' GROUP BY b2.remito_id) ultimo ON ultimo.remito_id=r.id WHERE er.nombre='Verificado'\n          UNION ALL SELECT v.fecha,v.local_id,l.producto_id,-l.cantidad,'Venta',v.numero_comprobante FROM venta v JOIN detalle_venta l ON l.venta_id=v.id\n          UNION ALL SELECT d.fecha,v.local_id,l.producto_id,l.cantidad,'Devolución apta','D-'||d.id FROM devolucion d JOIN venta v ON v.id=d.venta_id JOIN detalle_devolucion l ON l.devolucion_id=d.id)\n          SELECT m.fecha,e.nombre establecimiento,p.codigo,p.nombre producto,m.cantidad,m.concepto,m.referencia\n          FROM movimientos m JOIN establecimiento e ON e.id=m.establecimiento_id JOIN producto p ON p.id=m.producto_id\n          WHERE m.fecha>=:desde AND m.fecha<:hasta AND (:local IS NULL OR m.establecimiento_id=:local) ORDER BY m.fecha DESC",
            {"desde": since, "hasta": until, "local": local},
            StockMovementResponse,
        )

    def generate(
        self, since: str, until: str, local: int | None = None
    ) -> ReportDataResponse:
        params = {"desde": since, "hasta": until, "local": local}
        cash = self.query(
            "WITH operaciones AS (\n          SELECT v.fecha,v.local_id,v.metodo_pago_id,v.total bruto,0 reintegro FROM venta v\n          UNION ALL SELECT d.fecha,v.local_id,d.metodo_reintegro_id,0,SUM(l.cantidad*l.importe_unitario)\n          FROM devolucion d JOIN venta v ON v.id=d.venta_id JOIN detalle_devolucion l ON l.devolucion_id=d.id GROUP BY d.id)\n          SELECT e.nombre local,m.nombre medio_pago,SUM(o.bruto) bruto,SUM(o.reintegro) reintegros,SUM(o.bruto-o.reintegro) neto\n          FROM operaciones o JOIN establecimiento e ON e.id=o.local_id JOIN metodo_pago m ON m.id=o.metodo_pago_id\n          WHERE o.fecha>=:desde AND o.fecha<:hasta AND (:local IS NULL OR o.local_id=:local) GROUP BY o.local_id,o.metodo_pago_id ORDER BY local,medio_pago",
            params,
            SalesByPaymentResponse,
        )
        ranking = self.query(
            "WITH operaciones AS (\n          SELECT v.fecha,v.local_id,l.producto_id,l.cantidad unidades,l.cantidad*(l.precio_unitario-l.descuento_aplicado) ingreso,l.cantidad*l.costo_unitario costo\n          FROM venta v JOIN detalle_venta l ON l.venta_id=v.id\n          UNION ALL SELECT d.fecha,v.local_id,dl.producto_id,-dl.cantidad,-dl.cantidad*dl.importe_unitario,-dl.cantidad*vl.costo_unitario\n          FROM devolucion d JOIN venta v ON v.id=d.venta_id JOIN detalle_devolucion dl ON dl.devolucion_id=d.id\n          JOIN detalle_venta vl ON vl.venta_id=v.id AND vl.producto_id=dl.producto_id)\n          SELECT p.codigo,p.nombre producto,SUM(o.unidades) unidades_netas,SUM(o.ingreso) ingreso_neto,SUM(o.costo) costo_neto,\n          SUM(o.ingreso-o.costo) margen_estimado FROM operaciones o JOIN producto p ON p.id=o.producto_id\n          WHERE o.fecha>=:desde AND o.fecha<:hasta AND (:local IS NULL OR o.local_id=:local)\n          GROUP BY p.id ORDER BY unidades_netas DESC,ingreso_neto DESC",
            params,
            ProductRankingResponse,
        )
        rejects = self.query(
            "SELECT e.nombre destino,b.id bulto_id,r.numero_remito,ev.fecha,ev.observacion motivo,\n          SUM(l.cantidad) unidades,SUM(l.cantidad*p.costo_referencia) valor_referencia\n          FROM cambio_estado_bulto ev JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id JOIN bulto b ON b.id=ev.bulto_id\n          JOIN remito r ON r.id=b.remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id JOIN establecimiento e ON e.id=o.establecimiento_solicitante_id\n          JOIN detalle_bulto l ON l.bulto_id=b.id JOIN producto p ON p.id=l.producto_id\n          WHERE eb.nombre='Rechazado' AND ev.fecha>=:desde AND ev.fecha<:hasta AND (:local IS NULL OR e.id=:local)\n          GROUP BY b.id ORDER BY ev.fecha DESC",
            params,
            RejectedPackageResponse,
        )
        times = self.query(
            "WITH tiempos AS (\n          SELECT b.id,o.establecimiento_solicitante_id destino_id,\n          MIN(CASE WHEN eb.nombre='En tránsito' THEN ev.fecha END) salida,MIN(CASE WHEN eb.nombre='Recibido' THEN ev.fecha END) llegada\n          FROM bulto b JOIN remito r ON r.id=b.remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id\n          JOIN cambio_estado_bulto ev ON ev.bulto_id=b.id JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id GROUP BY b.id)\n          SELECT e.nombre destino,COUNT(t.llegada) recibidos,\n          ROUND(AVG(CASE WHEN t.llegada IS NOT NULL THEN (julianday(t.llegada)-julianday(t.salida))*24 END),2) horas_promedio,\n          SUM(CASE WHEN t.llegada IS NULL THEN 1 ELSE 0 END) en_transito\n          FROM tiempos t JOIN establecimiento e ON e.id=t.destino_id\n          WHERE t.salida>=:desde AND t.salida<:hasta AND (:local IS NULL OR e.id=:local) GROUP BY e.id",
            params,
            TransitSummaryResponse,
        )
        return ReportDataResponse(
            ventas=cash,
            productos=ranking,
            existencias=self.stock(local),
            rechazos=rejects,
            transito=times,
        )
