# Cumplimiento del TP

Referencia: `tema3.pdf`, páginas 1–2; propuesta del grupo 40 y `der_5_tp_dao.jpg`.

| Requisito | Implementación | Verificación |
| --- | --- | --- |
| Administrar CD y locales | Catálogo de establecimientos y domicilios | Un único CD, origen CD y destino local |
| Productos, categorías, proveedores, precios y mínimos | Catálogos e inventario | Identificadores normalizados, referencias, mínimos y bajas lógicas |
| Consolidar necesidades en una orden con origen y destino | Orden con varios productos y cantidades consolidadas por local | No admite repetición de producto ni origen/destino incorrectos |
| Empaquetar con remito y precinto | Orden → remitos → bultos → detalles | Reserva, límites de cantidades y unicidad de precinto |
| Registrar despacho | Acción permitida por State para bulto precintado | Verifica todos los precintos del remito y descuenta físico/reserva |
| Registrar recepción y verificar sello | Recepción e inspección separadas | Precinto intacto, número observado, remito y contenido |
| Venta, cobro, comprobante y devolución | Venta de varios productos, medio de pago, comprobante imprimible y devoluciones parciales | Cobro exacto, cantidades disponibles, precio/costo históricos y reintegros |
| No habilitar mercadería sin verificar | Acreditación del remito solo al completar todas las verificaciones | Prueba con dos bultos y prueba con un rechazo |
| Historial inmutable | cambio_estado_bulto, eventos en cada transición y triggers | Pruebas de UPDATE/DELETE rechazados |
| No sobreventa | Transacciones serializadas y validación en el servidor | Dos ventas concurrentes sobre la última unidad |
| No duplicar productos o proveedores | Código/CUIT normalizados y UNIQUE | Duplicados equivalentes rechazados |
| Validar devoluciones | Venta/producto original, cantidades acumuladas, aptitud y plazo | Devoluciones concurrentes, excedidas, vencidas o ajenas rechazadas |
| Al menos dos patrones | State y Strategy, con objetos polimórficos | Reglas de transición y devoluciones con descuento histórico |
| Al menos cuatro reportes no triviales | Cinco reportes agregados | Neto, costo histórico, filtros, tránsito y conciliación de inventario |

## Reportes implementados

1. Ventas e ingresos por local, medio y período: bruto, reintegros y neto.
2. Productos: unidades netas, ingresos netos, costo neto histórico y margen estimado.
3. Existencias: almacenado, reservado, disponible, mínimo, faltante y valorización actual.
4. Rechazos logísticos: bulto, destino, remito, fecha, motivo, unidades y valor de referencia.
5. Tránsito: promedio en horas por destino, bultos recibidos y todavía en tránsito, para la cohorte despachada en el período.

Los filtros de fechas no aplican al reporte de existencias actuales. Los reintegros se imputan en su propia fecha y las devoluciones se valorizan al precio histórico cobrado. El valor del rechazo no implica una pérdida confirmada.

## Validación reproducible

Desde `backend/`: `python -m unittest discover -s tests -t . -v`.

Las pruebas usan archivos SQLite temporales. Incluyen servicio y API HTTP mediante ASGITransport, esquemas de entrada, CORS/orígenes, historial inmutable, concurrencia real entre hilos y conciliación de movimientos con stock. El arnés de API ejecuta sus endpoints síncronos en el mismo hilo para no depender de sockets de notificación entre hilos dentro del entorno restringido. En producción FastAPI conserva su ejecución síncrona habitual.

Desde `frontend/`: `npm run build` comprueba TypeScript y genera la aplicación con Vite.

No se realizó una comprobación visual en navegador ni una conexión real entre los servidores: el entorno de elaboración restringe sockets. Esto no afecta las pruebas de la API dentro del proceso ni la compilación del frontend.

Las políticas que completan puntos no especificados se enumeran en `reglas_inventadas_o_asumidas.md`; no deben confundirse con requisitos literales de la cátedra.
