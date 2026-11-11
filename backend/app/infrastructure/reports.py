"""Consultas agregadas de lectura; sin reglas transaccionales de escritura."""
from sqlalchemy import text


class ReportsRepository:
    def __init__(self, database):
        self.database = database

    def query(self, sql, parameters):
        with self.database.engine.connect() as connection:
            return [dict(row) for row in connection.execute(text(sql), parameters).mappings()]

    def stock(self, local=None):
        return self.query('''SELECT e.id establecimiento_id,e.nombre establecimiento,p.id producto_id,p.codigo,p.nombre producto,
          COALESCE(x.almacenado_total,0) almacenado_total,COALESCE(x.reservado,0) reservado,
          COALESCE(x.almacenado_total-x.reservado,0) disponible,COALESCE(x.minimo_permitido,0) minimo_permitido,
          MAX(0,COALESCE(x.minimo_permitido-x.almacenado_total+x.reservado,0)) faltante,
          COALESCE(x.almacenado_total,0)*p.costo_referencia valorizacion
          FROM establecimiento e CROSS JOIN producto p LEFT JOIN existencia x ON x.establecimiento_id=e.id AND x.producto_id=p.id
          WHERE (:local IS NULL OR e.id=:local) ORDER BY faltante DESC,e.nombre,p.nombre''', {'local':local})

    def movements(self, since, until, local=None):
        return self.query('''WITH movimientos AS (
          SELECT c.fecha,e.id establecimiento_id,l.producto_id,l.cantidad,'Compra recibida' concepto,'C-'||c.id referencia
          FROM compra c JOIN estado_compra ec ON ec.id=c.estado_id JOIN detalle_compra l ON l.compra_id=c.id CROSS JOIN establecimiento e
          WHERE ec.nombre='Recibida' AND e.es_central=1
          UNION ALL SELECT ev.fecha,o.establecimiento_proveedor_id,l.producto_id,-l.cantidad,'Despacho','B-'||b.id
          FROM cambio_estado_bulto ev JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id JOIN bulto b ON b.id=ev.bulto_id
          JOIN remito r ON r.id=b.remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id JOIN detalle_bulto l ON l.bulto_id=b.id WHERE eb.nombre='En tránsito'
          UNION ALL SELECT ultimo.fecha,o.establecimiento_solicitante_id,l.producto_id,l.cantidad,'Recepción verificada',r.numero_remito
          FROM remito r JOIN estado_remito er ON er.id=r.estado_remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id
          JOIN bulto b ON b.remito_id=r.id JOIN detalle_bulto l ON l.bulto_id=b.id
          JOIN (SELECT b2.remito_id,MAX(ev.fecha) fecha FROM cambio_estado_bulto ev JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id JOIN bulto b2 ON b2.id=ev.bulto_id WHERE eb.nombre='Verificado' GROUP BY b2.remito_id) ultimo ON ultimo.remito_id=r.id WHERE er.nombre='Verificado'
          UNION ALL SELECT v.fecha,v.local_id,l.producto_id,-l.cantidad,'Venta',v.numero_comprobante FROM venta v JOIN detalle_venta l ON l.venta_id=v.id
          UNION ALL SELECT d.fecha,v.local_id,l.producto_id,l.cantidad,'Devolución apta','D-'||d.id FROM devolucion d JOIN venta v ON v.id=d.venta_id JOIN detalle_devolucion l ON l.devolucion_id=d.id)
          SELECT m.fecha,e.nombre establecimiento,p.codigo,p.nombre producto,m.cantidad,m.concepto,m.referencia
          FROM movimientos m JOIN establecimiento e ON e.id=m.establecimiento_id JOIN producto p ON p.id=m.producto_id
          WHERE m.fecha>=:desde AND m.fecha<:hasta AND (:local IS NULL OR m.establecimiento_id=:local) ORDER BY m.fecha DESC''',{'desde':since,'hasta':until,'local':local})

    def generate(self, since, until, local=None):
        params = {'desde':since,'hasta':until,'local':local}
        cash = self.query('''WITH operaciones AS (
          SELECT v.fecha,v.local_id,v.metodo_pago_id,v.total bruto,0 reintegro FROM venta v
          UNION ALL SELECT d.fecha,v.local_id,d.metodo_reintegro_id,0,SUM(l.cantidad*l.importe_unitario)
          FROM devolucion d JOIN venta v ON v.id=d.venta_id JOIN detalle_devolucion l ON l.devolucion_id=d.id GROUP BY d.id)
          SELECT e.nombre local,m.nombre medio_pago,SUM(o.bruto) bruto,SUM(o.reintegro) reintegros,SUM(o.bruto-o.reintegro) neto
          FROM operaciones o JOIN establecimiento e ON e.id=o.local_id JOIN metodo_pago m ON m.id=o.metodo_pago_id
          WHERE o.fecha>=:desde AND o.fecha<:hasta AND (:local IS NULL OR o.local_id=:local) GROUP BY o.local_id,o.metodo_pago_id ORDER BY local,medio_pago''',params)
        ranking = self.query('''WITH operaciones AS (
          SELECT v.fecha,v.local_id,l.producto_id,l.cantidad unidades,l.cantidad*(l.precio_unitario-l.descuento_aplicado) ingreso,l.cantidad*l.costo_unitario costo
          FROM venta v JOIN detalle_venta l ON l.venta_id=v.id
          UNION ALL SELECT d.fecha,v.local_id,dl.producto_id,-dl.cantidad,-dl.cantidad*dl.importe_unitario,-dl.cantidad*vl.costo_unitario
          FROM devolucion d JOIN venta v ON v.id=d.venta_id JOIN detalle_devolucion dl ON dl.devolucion_id=d.id
          JOIN detalle_venta vl ON vl.venta_id=v.id AND vl.producto_id=dl.producto_id)
          SELECT p.codigo,p.nombre producto,SUM(o.unidades) unidades_netas,SUM(o.ingreso) ingreso_neto,SUM(o.costo) costo_neto,
          SUM(o.ingreso-o.costo) margen_estimado FROM operaciones o JOIN producto p ON p.id=o.producto_id
          WHERE o.fecha>=:desde AND o.fecha<:hasta AND (:local IS NULL OR o.local_id=:local)
          GROUP BY p.id ORDER BY unidades_netas DESC,ingreso_neto DESC''',params)
        rejects = self.query('''SELECT e.nombre destino,b.id bulto_id,r.numero_remito,ev.fecha,ev.observacion motivo,
          SUM(l.cantidad) unidades,SUM(l.cantidad*p.costo_referencia) valor_referencia
          FROM cambio_estado_bulto ev JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id JOIN bulto b ON b.id=ev.bulto_id
          JOIN remito r ON r.id=b.remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id JOIN establecimiento e ON e.id=o.establecimiento_solicitante_id
          JOIN detalle_bulto l ON l.bulto_id=b.id JOIN producto p ON p.id=l.producto_id
          WHERE eb.nombre='Rechazado' AND ev.fecha>=:desde AND ev.fecha<:hasta AND (:local IS NULL OR e.id=:local)
          GROUP BY b.id ORDER BY ev.fecha DESC''',params)
        times = self.query('''WITH tiempos AS (
          SELECT b.id,o.establecimiento_solicitante_id destino_id,
          MIN(CASE WHEN eb.nombre='En tránsito' THEN ev.fecha END) salida,MIN(CASE WHEN eb.nombre='Recibido' THEN ev.fecha END) llegada
          FROM bulto b JOIN remito r ON r.id=b.remito_id JOIN orden_reposicion o ON o.id=r.orden_reposicion_id
          JOIN cambio_estado_bulto ev ON ev.bulto_id=b.id JOIN estado_bulto eb ON eb.id=ev.estado_bulto_id GROUP BY b.id)
          SELECT e.nombre destino,COUNT(t.llegada) recibidos,
          ROUND(AVG(CASE WHEN t.llegada IS NOT NULL THEN (julianday(t.llegada)-julianday(t.salida))*24 END),2) horas_promedio,
          SUM(CASE WHEN t.llegada IS NULL THEN 1 ELSE 0 END) en_transito
          FROM tiempos t JOIN establecimiento e ON e.id=t.destino_id
          WHERE t.salida>=:desde AND t.salida<:hasta AND (:local IS NULL OR e.id=:local) GROUP BY e.id''',params)
        return {'ventas':cash,'productos':ranking,'existencias':self.stock(local),'rechazos':rejects,'transito':times}
