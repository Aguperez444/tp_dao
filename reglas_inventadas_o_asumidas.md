# Reglas inventadas o asumidas

Base de trabajo: `tema3.pdf`, `der_5_tp_dao.jpg` y `Presentacion-grupo-40.docx`. Estas decisiones completan aspectos que esos documentos no especifican. No se presentan como exigencias de la cátedra. Si se cambia una política, deben ajustarse los servicios y las pruebas que la cubren.

## Organización y datos maestros

| Decisión adoptada | Justificación |
| --- | --- |
| Existe un único centro de distribución y varios locales. El tipo del establecimiento no puede cambiar después del alta. | El contexto menciona un CD central. Cambiar el tipo posteriormente invalidaría el significado de sus operaciones históricas. |
| Los establecimientos requieren domicilio; se administran provincia, ciudad y domicilio. | Respeta las relaciones del DER entregado, sin reemplazarlas por una dirección de texto libre. |
| Los nombres de establecimientos y categorías no se repiten, sin distinguir mayúsculas. En ciudades, el nombre es único dentro de su provincia. | Evita confusiones al seleccionar destinos y referencias. Productos y proveedores pueden compartir nombre si tienen identificadores distintos. |
| El código de producto se guarda sin espacios externos y en mayúsculas. El CUIT se guarda sin espacios ni guiones, con 11 dígitos. | Define cómo detectar duplicados equivalentes. El CUIT se valida por formato y longitud; no se consulta un padrón ni se comprueba su situación fiscal. |
| Productos y proveedores se desactivan con `esta_activo`; no se borran. Los demás maestros se pueden editar, pero no eliminar desde la API. | Permite conservar relaciones históricas. No se agregó un atributo de baja al establecimiento porque no está en el DER. |
| Los catálogos de estados y medios de pago se inicializan y no admiten edición desde la API. Los motivos de devolución sí se administran. | Evita renombrar estados que controlan el comportamiento del sistema; mantiene una lista de motivos extensible. |
| Las ventas se registran a consumidor anónimo, sin cuenta de cliente. | El DER no contiene clientes; no se inventa una gestión de clientes frecuentes, que el enunciado considera opcional. |

## Cantidades, importes y fechas

| Decisión adoptada | Justificación |
| --- | --- |
| Todas las cantidades son unidades enteras positivas; los mínimos pueden ser cero. | Se trabaja con mercadería por unidad, sin fraccionamiento por peso o volumen. |
| El límite de cantidad por línea y de mínimo configurable es 1.000.000; cada operación admite hasta 100 líneas. | Son límites técnicos de validación, no reglas comerciales de la cátedra. Evitan solicitudes desproporcionadas para una aplicación académica local. |
| Precio de venta mayor que cero; costos no negativos. Importes con hasta dos decimales, máximo $999.999.999,99; la misma cota se aplica al total de una venta. | Acota el manejo monetario y excluye ventas gratuitas no contempladas. Los costos cero permiten ejemplos o mercadería bonificada. |
| La moneda es el peso argentino (ARS). La API recibe importes en pesos como cadenas decimales y devuelve importes en centavos enteros. SQLite también guarda centavos. | Evita errores de punto flotante; el frontend convierte únicamente para presentación. La API también admite números decimales JSON válidos. |
| Fechas de operaciones y eventos generadas por el servidor en UTC, con hora y fracciones de segundo. Los filtros de reportes usan días UTC completos, incluyendo ambos extremos seleccionados. | Mantiene una referencia temporal común y permite calcular el tránsito. La interfaz muestra la hora de operaciones en la zona del navegador e identifica los filtros UTC. |
| Los movimientos financieros se imputan en la fecha de cada operación: una devolución posterior no reescribe el ingreso del día de venta. | Permite explicar ingresos netos de cada período y conciliar reintegros. |

## Compras e inventario

| Decisión adoptada | Justificación |
| --- | --- |
| Toda compra abastece al único CD; su destino se infiere sin agregar una FK a `compra`. | La entidad del DER no contiene establecimiento receptor y el contexto centraliza el abastecimiento. |
| Las compras pasan de Pendiente a Recibida. Solo se reciben completas y una sola vez. La fecha de la compra pasa a ser la de recepción al confirmarla. | Hace explícito el momento en que ingresa stock usando el único campo `fecha` del DER. No se incluyen recepciones parciales ni conservación de una fecha separada de pedido. |
| El costo de una compra se conserva en su detalle, pero no modifica automáticamente `producto.costo_referencia`. Este último lo administra el operador. | No se prescribe un método de valuación o promedio ponderado; se evita inventar un cálculo contable implícito. |
| `almacenado_total` contiene únicamente unidades admitidas para operar. Disponible = almacenado_total − reservado. Lo recibido sin verificar continúa representado por los bultos, fuera de la existencia habilitada. | Permite cumplir la prohibición de vender mercadería sin verificar sin agregar una columna de cuarentena al DER. |
| Los mínimos se definen por establecimiento y producto; si no se configuraron, valen cero. | Aprovecha la entidad `existencia`, ya que cada local puede tener necesidades diferentes. |
| La valorización de existencias usa almacenado_total × costo_referencia actual, incluidas las unidades reservadas que aún están en el CD. No incluye mercadería en tránsito o cuarentena. | Es una estimación operativa actual, no un balance del inventario total de la empresa ni una valuación contable FIFO. |
| Los movimientos se reconstruyen a partir de compras recibidas, eventos de despacho/verificación, ventas y devoluciones. No se agregó una tabla `movimiento`. | Conserva el DER. Las reservas se muestran por separado y no se cuentan como entradas o salidas físicas. |

## Reposición, remitos y bultos

| Decisión adoptada | Justificación |
| --- | --- |
| Las necesidades se consolidan manualmente en una orden para un único local, con una línea por producto. No se persisten solicitudes previas independientes. | El DER tiene orden y detalle de reposición, pero no una entidad de solicitud. La pantalla permite cargar las necesidades ya consolidadas. |
| En todas las operaciones con detalles, un producto aparece una sola vez; sus unidades deben consolidarse en esa línea. | Evita ambigüedad en cantidades e importes y permite vincular cada devolución a una única línea vendida mediante venta + producto, tal como está modelado. |
| Una orden puede tener varios remitos y un remito varios bultos. Se permite repartir un producto entre bultos y despachar una orden en entregas parciales. | Respeta la cardinalidad del DER y permite preparar envíos con el stock disponible sin esperar a completar toda la orden. |
| Solo puede haber un remito Pendiente de preparación por orden. Para emitir el siguiente se debe iniciar el despacho del anterior. No se agregan bultos a un remito cuyo despacho ya comenzó. | Evita remitos vacíos sobrantes y cambios de contenido durante el transporte. No impide preparar otra entrega después de iniciar la anterior. |
| Preparar un bulto reserva stock en el CD. Despacharlo reduce simultáneamente el almacenado y la reserva. | Evita comprometer las mismas unidades en varios envíos y conserva el stock físico hasta la salida real. |
| La suma de bultos de todos los remitos no puede superar lo solicitado por producto, incluidos los bultos rechazados. | Un rechazo no se interpreta como una nueva solicitud. Su reposición se documenta mediante una orden nueva, conservando la original. |
| Todos los bultos de un remito deben estar precintados antes del primer despacho de ese remito. No se exige embalar toda la orden. | El remito identifica un despacho con contenido cerrado; otros remitos pueden cubrir lo que falte de la orden. |
| El número de remito y el código de precinto son únicos, normalizados a mayúsculas. El precinto se asigna al precintar, no al preparar. | Permite identificar y verificar el sello de cada bulto y distingue las dos etapas obligatorias. |
| La inspección compara el número de remito, código e integridad del precinto y conformidad del contenido. Cualquier discrepancia rechaza el bulto y exige una observación. | Una comparación de código por sí sola no permite determinar que el sello esté intacto o que la entrega sea conforme. |
| Todos los bultos de un remito deben verificarse antes de acreditar stock de ese remito. Un solo rechazo bloquea la acreditación del remito completo, incluso de sus bultos verificados. | Es una política conservadora elegida por el grupo para resolver entregas parcialmente conformes. La consigna exige verificar remito y contenedor, pero no establece expresamente esta política colectiva. |
| El rechazo no vuelve automáticamente la mercadería al CD ni la convierte en pérdida definitiva. Queda en cuarentena para resolución fuera del alcance. | Evita inventar una devolución física o una merma que todavía no se produjo. El reporte muestra rechazo y valor estimado, no pérdida confirmada. |
| El estado del remito y el de la orden se calculan a partir de los bultos y cantidades; no se editan manualmente. | Evita que un operador marque una entrega completa sin cumplir sus verificaciones. |
| Se implementa State con Preparado → Precintado → En tránsito → Recibido → Verificado/Rechazado. Los terminales no admiten nuevas acciones y los eventos son de solo inserción. | El ciclo está exigido por la consigna; la elección de State y la protección con triggers concretan ese requisito. El responsable es un nombre declarado por el operador. |
| No se implementan cancelación, reapertura ni eliminación de órdenes, remitos, bultos, compras o ventas. | El enunciado no define sus efectos sobre reservas y comprobantes. Se preserva la historia; una operación ya registrada no se elimina para corregirla. |

## Ventas, precios y devoluciones

| Decisión adoptada | Justificación |
| --- | --- |
| Una venta se cobra completamente con un solo medio: Efectivo, Tarjeta o Transferencia. El importe cobrado debe coincidir exactamente con el total. | Respeta `venta.metodo_pago_id`. No se inventa una tabla de pagos, cobros combinados, crédito o cálculo de vuelto. |
| Los medios de pago son simulados y no se integran con bancos ni procesadores. | La materia evalúa el dominio; no se recibieron credenciales ni requisitos de integración. |
| Strategy ofrece precio de lista o descuento general del 10%, seleccionado para cada venta. El descuento se redondea por unidad al centavo más cercano, con mitades hacia arriba. | Es una familia pequeña de políticas que permite demostrar Strategy con una función concreta. El porcentaje y el redondeo no están fijados por la consigna. |
| `precio_unitario` conserva el precio de lista; `descuento_aplicado` es un importe monetario unitario en centavos, no un porcentaje. Subtotal = cantidad × (precio_unitario − descuento_aplicado). | El DER no aclara la unidad del descuento. Guardar el importe permite reconstruir exactamente lo cobrado. |
| `costo_unitario` copia el costo de referencia vigente al vender. El servidor calcula y guarda todos los valores históricos; el cliente no puede enviarlos. | Aprovecha el nuevo atributo del DER y evita que cambios de catálogo o del frontend alteren márgenes anteriores. No se asume FIFO ni costo promedio. |
| Los comprobantes de venta se numeran V-00000001 y los de devolución D-00000001, a partir del identificador de la operación. Son internos, sin validez fiscal. | Ofrece una referencia única e imprimible sin simular integración con ARCA. El número de devolución se deriva, sin agregar una columna al DER. |
| Se aceptan devoluciones hasta 30 × 24 horas después de la venta, completas o parciales, con motivo y explicación obligatorios. | Define un plazo defendible y acotado que el enunciado deja a criterio del grupo. |
| Solo se aceptan productos de esa venta, sin superar vendido − devuelto acumulado. Se admite devolver un producto que luego fue desactivado. | La operación original determina el derecho de devolución; una baja del catálogo no debe invalidarla. |
| Solo se registran devoluciones inspeccionadas y aptas para reventa. Todas vuelven al stock verificado del mismo local que vendió. | El DER no contiene aptitud, merma ni disposición de mercadería devuelta. Se exige confirmación previa en lugar de almacenar un resultado que no puede representarse. Las devoluciones dañadas quedan fuera del alcance de esta versión. |
| El reintegro usa precio unitario − descuento unitario de la venta original y admite seleccionar un medio de reintegro distinto del cobro. | Se devuelve el importe realmente pagado, nunca el precio actual. El DER contempla una referencia separada para el medio de reintegro. |
| El margen bruto estimado es ingreso neto − costo histórico neto. Una devolución apta revierte ambos conceptos. No incluye impuestos, gastos operativos ni comisiones. | Permite explicar qué resultado económico se calcula sin presentarlo como utilidad contable. |

## Reportes y condiciones técnicas

| Decisión adoptada | Justificación |
| --- | --- |
| Se implementan cinco reportes: ingresos por local/medio, productos y margen, existencias/mínimos, rechazos y tránsito. | La consigna exige al menos cuatro; los cinco elegidos cubren logística, stock y resultado económico. |
| El tránsito se mide desde En tránsito hasta Recibido. El filtro selecciona bultos despachados en el período; se promedian solo los recibidos y se cuentan aparte los que aún viajan. | Define una cohorte coherente y evita promediar bultos sin fecha final. No incluye preparación ni inspección. |
| Las operaciones de escritura se serializan en SQLite con BEGIN IMMEDIATE. Validaciones, cambios de stock y registros se confirman o revierten juntos. | Evita doble venta, doble recepción, doble verificación y exceso de devoluciones por solicitudes concurrentes. |
| Aplicación académica local, sin autenticación. El responsable de cada evento se declara por nombre; no es una identidad verificada. Los triggers impiden editar el historial desde la aplicación, pero no protegen frente a un administrador del archivo SQLite. | La consigna no define usuarios ni roles. Se explicita el límite de la auditoría y no se inventa una garantía de identidad o inviolabilidad. |
| Las pantallas se sirven desde un frontend independiente React/TypeScript; FastAPI solo expone JSON. La demo se puede cargar únicamente si no hay datos de negocio y su carga es transaccional. | Mantiene la separación solicitada y evita sobrescribir trabajo del usuario al explorar ejemplos. |
| La base anterior se conserva como respaldo separado y no se migra automáticamente. | Su esquema era distinto del DER; reinterpretar operaciones sin reglas de migración podría perder información. La nueva aplicación no lee ni modifica ese respaldo. |
