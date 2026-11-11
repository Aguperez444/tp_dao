# Respuestas para la presentación — Tema 3, grupo 40

Guía basada en el enunciado `docs/tema3.pdf`, la propuesta `Presentacion-grupo-40.docx`, la documentación y el código actual de **Nexo**. Las respuestas están redactadas para poder explicarlas oralmente y acompañarlas con una demostración.

## 1. Explicar primero el enunciado y la solución

**¿Qué pide el trabajo?**

El tema 3 plantea un comercio con un centro de distribución (CD) y varios locales. El CD se abastece y envía mercadería a los locales; cada local controla sus existencias, solicita reposición y vende al público. El sistema debe integrar compras, inventario, logística, ventas, cobros, comprobantes y devoluciones.

La regla más importante es que **la mercadería recibida en un local no se puede vender hasta verificar los bultos y su remito**. También se exige trazabilidad inmutable del bulto, evitar sobreventas y duplicados, validar devoluciones, aplicar al menos dos patrones y presentar al menos cuatro reportes no triviales.

**¿Cómo lo resolvimos?**

> Desarrollamos Nexo para seguir la mercadería desde la compra al proveedor hasta la venta o devolución. Organizamos la página por operaciones: Catálogo, Compras, Reposición y bultos, Ventas y devoluciones, Inventario y Reportes. El backend valida cada operación y actualiza los datos en una transacción. Aplicamos State al ciclo del bulto y Strategy al cálculo del precio de venta.

La interfaz está hecha con React y TypeScript; se comunica por una API JSON con FastAPI. La persistencia utiliza SQLAlchemy y SQLite. El backend separa API, aplicación, dominio e infraestructura para distribuir responsabilidades.

**Alcance que conviene aclarar:** es una aplicación académica local, sin autenticación; los pagos son simulados y los comprobantes son internos, sin validez fiscal. No se implementan clientes frecuentes, cuentas corrientes, lotes ni vencimientos.

Referencias: [enunciado](docs/tema3.pdf), [arquitectura](docs/arquitectura.md), [aplicación](backend/app/main.py) y [navegación](frontend/src/App.tsx).

## 2. Objetos del dominio: ¿qué modelamos?

> Modelamos los conceptos del negocio necesarios para abastecer locales y vender mercadería: productos, proveedores, establecimientos, existencias, compras, órdenes de reposición, remitos, bultos, ventas y devoluciones. También representamos sus detalles, estados y datos de ubicación.

No modelamos solamente pantallas: representamos operaciones y relaciones del comercio. Por ejemplo, un bulto pertenece a un remito, el remito corresponde a una orden y la orden identifica el CD de origen y el local de destino.

El modelo persistente contiene **27 entidades/tablas**. Además existen objetos que representan comportamiento, como `Package`, los estados concretos del bulto y las políticas de precios.

Una precisión sobre la implementación: las entidades persistentes están en `infrastructure/models.py`; gran parte de las reglas se coordina en los servicios de aplicación. Los objetos State y Strategy están en `domain/`. No todas las reglas viven como métodos dentro de las entidades ORM.

## 3. Entidades: atributos, relaciones y responsabilidades

Una entidad tiene identidad propia y continuidad en el tiempo. Un producto sigue siendo el mismo aunque cambie su nombre o precio; una venta conserva su identidad y sus importes originales aunque después cambie el catálogo.

| Entidad o grupo | Qué representa y datos principales | Relaciones relevantes |
| --- | --- | --- |
| `Producto` | Mercadería: código único, nombre, descripción, precio, costo de referencia y condición de activo. | Pertenece a una categoría; participa en existencias y detalles de operaciones. |
| `Categoria` | Clasificación de productos. | Una categoría puede agrupar varios productos. |
| `Proveedor` | Quien abastece al negocio: CUIT único, nombre y condición de activo. | Un proveedor puede tener varias compras. |
| `Establecimiento` | CD o local, con nombre, domicilio e indicador `es_central`. | Tiene existencias y participa como origen o destino logístico. Las ventas pertenecen a locales. |
| `Provincia`, `Ciudad`, `Domicilio` | Ubicación de los establecimientos. | Una ciudad pertenece a una provincia; un domicilio a una ciudad. |
| `Existencia` | Stock de un producto en un establecimiento: almacenado, reservado y mínimo permitido. | Hay como máximo un registro por pareja establecimiento/producto. Disponible = almacenado − reservado. |
| `Compra`, `DetalleCompra` | Abastecimiento desde un proveedor; cada detalle indica producto, cantidad y costo unitario. | Una compra tiene varios detalles y un estado. Su recepción incrementa stock del CD. |
| `OrdenReposicion`, `DetalleReposicion` | Necesidad consolidada de un local: origen, destino, fecha y productos solicitados. | Una orden admite varios detalles y varios remitos para entregas parciales. |
| `Remito` | Documento de despacho con número único, fecha y estado. | Pertenece a una orden y agrupa bultos. |
| `Bulto`, `DetalleBulto` | Unidad física preparada para enviar; código de precinto, estado del precinto y estado del bulto. | Un bulto pertenece a un remito y contiene productos con cantidades. |
| `CambioEstadoBulto` | Registro histórico de estado, fecha, responsable y observación. | Cada evento corresponde a un bulto. El historial se agrega y no se edita ni elimina desde la aplicación. |
| `Venta`, `DetalleVenta` | Operación de un local, con medio de pago, fecha, total y comprobante. | Los detalles guardan producto, cantidad, precio, descuento monetario unitario y costo histórico. |
| `Devolucion`, `DetalleDevolucion` | Reintegro vinculado a una venta: motivo, explicación, fecha, medio de reintegro, productos y cantidades. | Una venta puede tener varias devoluciones parciales, sin exceder las unidades vendidas. |
| `MetodoPago`, `Motivo` | Referencias para cobros/reintegros y motivos de devolución. | Se vinculan con ventas o devoluciones según corresponda. |
| `EstadoCompra`, `EstadoReposicion`, `EstadoRemito`, `EstadoPrecinto`, `EstadoBulto` | Catálogos de estados persistidos. | Identifican la situación de cada operación. El comportamiento del bulto lo implementan las clases de State. |

**Relaciones que conviene mostrar en el DER:**

- `Proveedor → Compra → DetalleCompra → Producto`.
- `OrdenReposicion → Remito → Bulto → DetalleBulto → Producto`.
- `Bulto → CambioEstadoBulto`.
- `Establecimiento → Existencia ← Producto`.
- `Establecimiento → Venta → DetalleVenta → Producto`.
- `Venta → Devolucion → DetalleDevolucion → Producto`.

Los detalles permiten registrar varios productos por operación y conservar datos propios de esa operación, como cantidad y precio histórico. El stock pertenece a `Existencia`, porque un mismo producto puede tener cantidades diferentes en cada local.

Referencias: [entidades persistentes](backend/app/infrastructure/models.py) y [DER](docs/der_5_tp_dao.jpg).

## 4. ¿Dónde usamos herencia y por qué?

### Herencia para el comportamiento del bulto

En [shipping.py](backend/app/domain/shipping.py), `PackageState` es una clase abstracta que define `advance(action)`. Heredan de ella:

- `Prepared`: Preparado.
- `Sealed`: Precintado.
- `InTransit`: En tránsito.
- `Received`: Recibido.
- `Verified`: Verificado.
- `Rejected`: Rechazado.

Cada subclase responde al mismo método y decide qué transición permite. Por ejemplo, `Prepared` solo permite precintar y `Received` permite verificar o rechazar. Esto es polimorfismo: `Package` trabaja con un `PackageState` sin necesitar conocer cada clase concreta.

**¿Por qué?** Porque las acciones válidas cambian según el estado y queremos concentrar cada comportamiento en su clase. `Package` mantiene su estado por composición y delega la acción en él; el bulto no hereda de sus estados.

### Herencia para políticas de precio

En [pricing.py](backend/app/domain/pricing.py), `PricingPolicy` declara el método abstracto `discount(price_cents)`. `ListPrice` devuelve descuento cero y `TenPercentDiscount` calcula un 10% de descuento.

**¿Por qué?** Ambas políticas cumplen el mismo contrato y pueden intercambiarse en `PriceCalculator`. Permite incorporar otra política sin cambiar el algoritmo que recorre los productos de la venta; sí habría que registrarla y habilitar su selección.

### Herencia para reutilizar infraestructura y servicios

- En [models.py](backend/app/infrastructure/models.py), `Base` hereda de `DeclarativeBase` de SQLAlchemy y las entidades heredan de `Base` para su mapeo. El mixin `Named` comparte `id` y `nombre` entre categorías, provincias, estados, medios de pago y motivos. Esto reutiliza atributos; no expresa una jerarquía del negocio entre esas entidades.
- En [common.py](backend/app/application/common.py), `Service` comparte la fábrica de unidades de trabajo y validaciones. Lo extienden `CatalogService`, `PurchasingService`, `LogisticsService` y `SalesService`. `ReportingService` recibe su repositorio directamente y no hereda de `Service`.
- En [errors.py](backend/app/domain/errors.py), `BusinessError` hereda de `ValueError` y `NotFoundError` de `BusinessError`, para distinguir errores de negocio y recursos inexistentes.

**Aclaración para la defensa:** no existen subclases `Local` y `CentroDistribucion`. Ambos se representan mediante `Establecimiento` y el atributo `es_central`. Tampoco `SqlAlchemyRepository` hereda explícitamente del protocolo `Repository`: cumple su contrato por estructura.

## 5. ¿Qué patrones usamos y por qué?

### State: controlar el ciclo de vida del bulto

> Usamos State porque un bulto permite distintas acciones según su estado. No se puede despachar uno preparado ni verificar uno que todavía está en tránsito.

Participantes concretos:

- **Contexto:** `Package`, que mantiene un `PackageState`.
- **Abstracción:** `PackageState`.
- **Estados concretos:** `Prepared`, `Sealed`, `InTransit`, `Received`, `Verified` y `Rejected`.
- **Delegación:** `Package.execute(action)` llama a `state.advance(action)` y conserva el nuevo estado.

`LogisticsService.transition()` reconstruye el estado desde la persistencia, ejecuta la transición y coordina las validaciones externas, el stock y el historial en la misma transacción.

**Beneficio:** hace explícitas las transiciones válidas y rechaza saltos de estado. Tener una tabla de estados por sí sola no sería implementar State: acá existen objetos que encapsulan comportamiento.

### Strategy: elegir cómo calcular el precio

> Usamos Strategy porque podemos aplicar precio de lista o un descuento del 10% conservando el mismo proceso de venta.

Participantes concretos:

- **Contexto:** `PriceCalculator`.
- **Abstracción:** `PricingPolicy`.
- **Estrategias:** `ListPrice` y `TenPercentDiscount`.
- **Selección:** `policy_for()` crea la política elegida y `SalesService._quote()` la usa para calcular los detalles.

**Beneficio:** separa la política de descuento del registro de la venta. El detalle conserva lo cobrado para que una devolución use el precio histórico, aunque cambie el precio del producto.

Ejemplo: dos unidades de $100 con descuento del 10% cuestan $180. Si después se devuelve una, se reintegran $90.

`policy_for()` es una función de creación/selección; no hace falta presentarla como el patrón GoF Factory Method.

### Repository/DAO y Unit of Work: acceso a datos y consistencia

Los contratos están en [ports.py](backend/app/domain/ports.py). [SqlAlchemyRepository](backend/app/infrastructure/repository.py) encapsula el acceso a los registros y [SqlAlchemyUnitOfWork](backend/app/infrastructure/database.py) confirma o revierte una operación completa.

**¿Por qué?** Para que los servicios no dependan directamente del ORM y para que una operación no quede registrada a medias. Si falla la preparación de un producto del bulto, se revierten también las reservas que se habían hecho para los anteriores.

Las escrituras usan `BEGIN IMMEDIATE`: lectura, validación y modificación quedan dentro de una misma transacción, evitando que dos solicitudes vendan la última unidad o acrediten dos veces una recepción.

Para responder por los **dos patrones obligatorios**, conviene desarrollar primero State y Strategy. Repository/DAO y Unit of Work complementan la explicación.

## 6. Ciclo de vida que exige el TP

El objeto central evaluado es el **bulto/contenedor**. Su secuencia es:

```text
Preparado → Precintado → En tránsito → Recibido → Verificado
                                             └→ Rechazado
```

| Estado alcanzado | Acción y condición | Efecto sobre las existencias |
| --- | --- | --- |
| Preparado | Crear el bulto dentro de un remito pendiente, con cantidades de la orden y stock suficiente en el CD. | Reserva unidades del CD; disminuye su disponible, pero no su almacenado. |
| Precintado | Colocar un código único de precinto. | Mantiene la reserva. |
| En tránsito | Registrar despacho. Todos los bultos del remito deben estar precintados antes del primer despacho. | Descuenta del CD tanto almacenado como reservado por las unidades de ese bulto. |
| Recibido | Registrar llegada física al local. | Todavía no acredita unidades vendibles al local. |
| Verificado | Inspeccionar y confirmar código de precinto, remito, integridad del sello y conformidad del contenido. | Acredita el contenido de todo el remito solo cuando todos sus bultos están verificados. |
| Rechazado | La inspección encuentra alguna disconformidad; exige una observación. | Bloquea la acreditación de todo ese remito, incluso si otro bulto fue verificado. |

**Ejemplo para explicar la reserva:** si el CD tiene 100 unidades y prepara 10, queda con 100 almacenadas, 10 reservadas y 90 disponibles. Al despacharlas queda con 90 almacenadas, 0 reservadas y 90 disponibles. El local recibe las 10 como stock habilitado únicamente después de la verificación completa del remito.

Si el remito tiene dos bultos de cinco unidades, verificar el primero no suma cinco al local. La acreditación de diez ocurre al verificar el segundo, siempre que no haya rechazos.

Cada cambio agrega un evento con estado, fecha, responsable y observación. Dos triggers de SQLite impiden modificar o borrar esos eventos. El responsable es un nombre declarado por el operador; no hay autenticación de identidad.

`Verificado` y `Rechazado` son estados finales. La versión actual no implementa recuperación, reenvío ni disposición de mercadería rechazada. La cuarentena significa que esas unidades quedan fuera del stock vendible; no existe una entidad separada para administrarla.

### Ciclos relacionados

- **Compra:** Pendiente → Recibida. Crear la compra no acredita stock; recibirla lo acredita una sola vez en el CD.
- **Orden de reposición:** Pendiente → En preparación → En tránsito → Completada en el recorrido exitoso; puede quedar Con rechazos. Su estado se calcula a partir de cantidades asignadas y remitos.
- **Remito:** Pendiente → En tránsito → Recibido → Verificado en el recorrido exitoso; puede quedar Rechazado por alguno de sus bultos. Su estado es derivado y no se elige libremente en la pantalla.
- **Venta y devolución:** la venta confirma cobro, comprobante y descuento de stock juntos. La devolución se registra como una nueva operación vinculada a la venta original; repone unidades aptas y registra el reintegro.

Las devoluciones se admiten hasta 30 días, requieren productos aptos para reventa y no pueden superar lo vendido menos lo ya devuelto. Estas condiciones, el descuento del 10% y el bloqueo de todo el remito ante un rechazo son decisiones documentadas del grupo que concretan aspectos del enunciado.

Referencias: [State](backend/app/domain/shipping.py), [logística](backend/app/application/logistics.py), [ventas](backend/app/application/sales.py) y [reglas asumidas](docs/reglas_inventadas_o_asumidas.md).

## 7. Control del flujo de la página

### Recorrido recomendado para mostrar el sistema

1. **Resumen:** explicar qué integra Nexo y el recorrido de la mercadería. La demostración precargada se puede cargar únicamente en una base sin datos de negocio; si ya existen datos, usar los existentes o una base alternativa.
2. **Catálogo:** mostrar categoría, producto, proveedor y establecimientos. Para crear ubicaciones desde cero, seguir Provincia → Ciudad → Domicilio → Establecimiento. Registrar un CD y al menos un local.
3. **Compras:** crear una compra con sus productos, cantidades y costos. Mostrar que sigue Pendiente y aún no incrementa stock. Abrirla y confirmar la recepción.
4. **Inventario:** comprobar que el CD recibió las unidades.
5. **Reposición y bultos:** crear una orden indicando CD de origen y local de destino; generar su remito y preparar dos bultos. Mostrar las reservas y la trazabilidad inicial.
6. Precintar ambos bultos con códigos distintos. Despacharlos y mostrar el descuento de stock del CD.
7. Registrar la recepción física de ambos. Comprobar que el local todavía no tiene disponibles las unidades enviadas.
8. Inspeccionar el primer bulto con datos correctos: todavía no debe ingresar stock del remito. Inspeccionar el segundo: ahora deben acreditarse todas sus unidades al local.
9. **Ventas y devoluciones:** registrar una venta con varios productos, política de precio y medio de pago. El importe cobrado debe coincidir con el total. Al confirmar, el sistema abre el comprobante y permite imprimirlo.
10. Desde el comprobante, registrar una devolución parcial con motivo, medio de reintegro y confirmación de aptitud. Mostrar el stock recuperado y el reintegro asociado.
11. **Reportes:** mostrar ventas netas y margen, explicando cómo impacta la devolución.
12. En otra operación, mostrar un precinto roto y el rechazo con motivo. Comprobar que ese remito no suma stock al local. Si había stock anterior, podrá seguir vendiéndose ese stock; el bloqueo corresponde a las unidades del remito rechazado.

### ¿Qué se verificó en esta revisión?

Se ejecutaron **36 pruebas del backend y todas pasaron**, incluyendo el flujo completo por API: compra → recepción → orden → remito → bulto → precintado → despacho → recepción → inspección → venta → devolución → inventario/reportes.

También se comprobaron por pruebas las siguientes reglas:

- No saltar estados ni verificar directamente sin inspección.
- No acreditar stock hasta verificar todos los bultos del remito.
- Bloquear el remito completo ante un rechazo.
- No vender más de lo disponible, incluso ante dos ventas concurrentes.
- No acreditar dos veces una compra o una verificación.
- No repetir códigos de producto, CUIT equivalentes ni códigos de precinto.
- No devolver productos ajenos a la venta, cantidades excesivas o fuera de plazo.
- Conservar precios, descuentos y costos históricos.
- Revertir una operación completa si alguna de sus validaciones falla.
- Impedir edición y eliminación del historial de estados.

La compilación del frontend con `npm run build` también pasó, incluida la comprobación de TypeScript.

**Límite de la revisión:** se revisaron las rutas, formularios y estilos en código, y se probó el flujo del backend. No se realizó una prueba interactiva en navegador ni una evaluación visual renderizada. Por eso todavía corresponde ensayar el recorrido de clics, la impresión y la visualización en el equipo que se usará para exponer.

Comandos utilizados, con las dependencias disponibles en el Python del entorno:

```sh
# Desde backend/
python -m unittest discover -s tests -t . -v

# Desde frontend/
npm run build
```

Referencias: [pruebas de negocio](backend/tests/test_business.py), [pruebas de API](backend/tests/test_api.py) y [pantalla de logística](frontend/src/pages/Logistics.tsx).

## 8. Página simple, intuitiva y sin saturación visual

**Respuesta para la presentación:**

> Organizamos la interfaz por tareas del negocio y usamos una navegación estable. Las pantallas presentan una acción principal y abren formularios cuando se necesitan. En logística, cada bulto muestra la siguiente acción según su estado y deja la trazabilidad desplegable para consultar el detalle sin ocupar toda la pantalla. Usamos fondos claros, tarjetas blancas y una paleta de verdes, con avisos diferenciados para errores y rechazos.

Esto se observa en el código de la interfaz:

- Menú con secciones identificadas mediante texto e iconos y marca de sección activa.
- Acciones como “Nueva compra”, “Nueva reposición” y “Cobrar y emitir comprobante”.
- Formularios en ventanas de diálogo para concentrarse en una operación.
- Estados identificados con texto y color; el significado no depende solo del color.
- Mensajes que distinguen recepción física de verificación y explican cuándo se habilita el stock.
- Avisos de error, confirmación de guardado y bloqueo del envío mientras se procesa.
- Estilos para pantallas pequeñas e impresión del comprobante.

### Observaciones de usabilidad a tener en cuenta

Estas oportunidades se detectaron por lectura del código; **no se modificó la aplicación como parte de esta revisión**:

| Observación | Consecuencia y mejora sugerida |
| --- | --- |
| El botón “Registrar despacho” aparece para un bulto precintado aunque otro del remito siga preparado. | El backend rechaza correctamente la operación, pero sería más claro deshabilitar el botón e indicar que faltan bultos por precintar. |
| “Registrar devolución” aparece también cuando todos los productos ya fueron devueltos o pasó el plazo. | El servidor valida, pero la interfaz podría deshabilitar la acción y explicar la razón antes de abrir el formulario. |
| En logística se muestran todas las órdenes y sus remitos/bultos sin búsqueda ni paginación. | Con más operaciones puede volverse extensa. Conviene agregar filtros o plegar órdenes terminadas. |
| Varios textos secundarios y etiquetas usan tamaños de 9–11 px y tonos claros. | Conviene comprobar legibilidad y contraste en navegador y con el proyector; posiblemente aumentar tamaños y oscurecer textos secundarios. |
| Los datos iniciales tienen dependencias entre catálogos. | Aunque existe una indicación para establecimientos, una guía de carga inicial facilitaría el primer uso. |

Referencias: [navegación](frontend/src/App.tsx), [estilos](frontend/src/styles.css), [logística](frontend/src/pages/Logistics.tsx) y [comprobante/devolución](frontend/src/pages/Sales.tsx).

## 9. Reportes que conviene poder explicar

Se implementaron **cinco**, superando el mínimo de cuatro:

| Reporte | Qué informa y por qué sirve |
| --- | --- |
| Ventas e ingresos | Cobros, reintegros y neto por local, medio de pago y período. Distingue lo vendido de lo efectivamente neto de devoluciones. |
| Productos y margen estimado | Unidades netas, ingresos netos, costo histórico neto y margen bruto estimado. Permite comparar productos. |
| Existencias y mínimos | Almacenado, reservado, disponible, mínimo, faltante y valorización al costo de referencia vigente. Permite detectar necesidad de reposición. |
| Rechazos logísticos | Bultos rechazados, remito, destino, fecha, motivo, unidades y valor de referencia. Permite analizar incidentes. |
| Tiempo de tránsito | Promedio de horas entre despacho y recepción física por destino, bultos recibidos y aún en tránsito, para los despachados en el período. Permite evaluar tiempos de entrega. |

No son simples listados: combinan operaciones, agrupaciones y cálculos. Los reportes económicos consideran devoluciones y el costo guardado al vender. Los reintegros se imputan en su propia fecha. El reporte de existencias muestra la situación actual, por lo que el período no aplica. Los filtros temporales se expresan en UTC.

**Margen bruto estimado = ingresos netos − costo histórico neto.** No incluye gastos, impuestos ni comisiones. El valor de un rechazo tampoco se presenta como una pérdida definitiva.

Referencias: [consultas](backend/app/infrastructure/reports.py) y [pantalla de reportes](frontend/src/pages/Reports.tsx).

## 10. División sugerida para hablar

La presentación del grupo identifica a Agustín Perez, Nazareno Derico Farrando y Lucas Gonzalo Cuello Arrigoni. Esta es una **propuesta de reparto para exponer**, no una afirmación sobre quién desarrolló cada parte.

| Integrante | Bloque sugerido | Qué puede mostrar |
| --- | --- | --- |
| Agustín Perez | Enunciado, objetivo, objetos, entidades y relaciones. | Resumen, catálogo y DER; explicar producto frente a existencia y orden frente a remito/bulto. |
| Nazareno Derico Farrando | Herencia, State, ciclo del bulto y trazabilidad. | Compra recibida, preparación, reserva, precintado, despacho, recepción, verificación y rechazo. |
| Lucas Gonzalo Cuello Arrigoni | Strategy, ventas, devoluciones, reportes y decisiones de interfaz. | Dos políticas de precio, comprobante, devolución parcial e impacto en stock e ingresos. |

Para coordinarse:

- Acordar quién maneja la computadora; los otros hablan en su turno.
- Usar una transición breve entre bloques: “Ahora vamos a mostrar cómo esas entidades participan en el envío de mercadería”.
- Si el profesor pregunta a alguien, dejar que esa persona termine su respuesta. Complementar después, sin hablar simultáneamente.
- Ensayar el mismo caso de negocio de principio a fin, con números conocidos y códigos de remito/precinto preparados.
- Todos deben poder explicar las reglas centrales, aunque no les toque presentarlas.

### Preguntas que cualquiera debería poder responder

- **¿Recibir equivale a verificar?** No. Recibir registra la llegada; inspeccionar determina conformidad o rechazo y puede habilitar stock cuando todo el remito está verificado.
- **¿Por qué no guardar stock directamente en Producto?** Porque depende del establecimiento; esa relación se representa mediante `Existencia`.
- **¿Por qué guardar el precio y el costo en DetalleVenta?** Para conservar los valores originales de la operación y calcular reintegros y márgenes históricos.
- **¿State y Strategy son lo mismo?** Comparten delegación por composición, pero resuelven problemas diferentes: State controla comportamiento y transiciones según el estado; Strategy intercambia una política de cálculo elegida para la venta.
- **¿Qué sucede si se verifica un bulto y se rechaza otro del mismo remito?** El remito queda rechazado y no se acredita su contenido al stock vendible.
- **¿Cómo se evita vender dos veces la última unidad?** Se vuelve a validar el disponible dentro de una transacción de escritura serializada antes de registrar la venta.
- **¿Qué reglas agregó el grupo?** Entre otras, devolución hasta 30 días, aceptación solo de productos aptos para reventa, descuento del 10% y un único medio de pago por venta. Están justificadas en el documento de reglas asumidas.
- **¿Hay una caja con apertura y cierre?** No hay una entidad ni un módulo de caja. Se registran cobros y reintegros asociados a operaciones, y se informa su efecto en ingresos.

## Fuentes principales

- [Enunciado del tema 3](docs/tema3.pdf).
- [Propuesta del grupo 40](Presentacion-grupo-40.docx).
- [DER](docs/der_5_tp_dao.jpg).
- [Arquitectura](docs/arquitectura.md).
- [Cumplimiento](docs/cumplimiento.md).
- [Reglas asumidas y sus justificaciones](docs/reglas_inventadas_o_asumidas.md).
- Código y pruebas enlazados en cada respuesta.
