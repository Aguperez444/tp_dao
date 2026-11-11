# Arquitectura y correspondencia con el DER

El proyecto usa React y TypeScript para presentación, FastAPI para HTTP, SQLAlchemy para persistencia y SQLite 3 como motor. La referencia del modelo es `der_5_tp_dao.jpg`; se implementan sus 27 tablas con los nombres y atributos del diagrama, incluido `detalle_venta.costo_unitario`. No se conservan las entidades adicionales del prototipo anterior.

```text
frontend/src/
  páginas y componentes React
           │ HTTP JSON /api
           ▼
backend/app/api/
  rutas FastAPI y esquemas Pydantic
           │ datos validados
           ▼
backend/app/application/
  servicios de catálogo, compras, logística, ventas y reportes
           │ contratos de repositorio y unidad de trabajo
           ├──► backend/app/domain/
           │      State, Strategy, importes y excepciones
           ▼
backend/app/infrastructure/
  ORM, repositorio, transacciones y consultas agregadas
           │
           ▼
        SQLite 3
```

## Responsabilidades

- **API / presentación HTTP:** valida tipos, límites y campos permitidos. Traduce errores de negocio a 409, recursos inexistentes a 404 y entradas inválidas a 422. Expone OpenAPI en `/docs` y `/openapi.json`. No contiene SQL ni decide efectos de stock.
- **Aplicación:** coordina las operaciones completas y sus reglas de consistencia. Recibe una fábrica de unidades de trabajo; no importa FastAPI ni SQLAlchemy. Los servicios se pueden utilizar en pruebas o en la carga de demo sin simular HTTP.
- **Dominio:** define errores, cálculo monetario y los objetos polimórficos de State y Strategy. No conoce HTTP, React, SQLite ni el ORM.
- **Infraestructura:** mapea el DER a tablas, implementa acceso a datos y unidad de trabajo. `ReportsRepository` concentra SQL de lectura con agregaciones; evita multiplicar ingresos al combinar ventas y detalles.
- **Frontend:** conserva el estado de formularios, presenta información y solicita operaciones. Los cálculos de pantalla son orientativos: los valores finales se obtienen en el servidor. No accede directamente a SQLite.

El repositorio genérico es interno, con una lista cerrada de modelos; no constituye una API genérica de escritura. Cada caso de uso conserva sus validaciones y la API solo permite los comandos expuestos.

## Transacciones y concurrencia

Cada escritura abre `BEGIN IMMEDIATE` antes de leer stock o cantidades devueltas. La validación y la modificación usan la misma conexión y se confirman juntas. Una segunda escritura espera el resultado de la primera y revalida los datos actuales. Las lecturas de servicios tienen transacción de lectura; los reportes ejecutan consultas agregadas de solo lectura.

No se usa una sesión ORM global ni se comparte una sesión entre solicitudes. Se habilitan claves foráneas y restricciones CHECK/UNIQUE. Dos triggers impiden UPDATE y DELETE sobre `cambio_estado_bulto`. Esta protección cubre el uso de la aplicación, no a un administrador capaz de cambiar el esquema del archivo.

## Patrones

**State:** `Package` mantiene un `PackageState` y delega `execute()` en `advance()`. Cada estado concreto define las acciones que admite y devuelve el siguiente estado. El servicio realiza verificaciones externas, persiste el nuevo estado y agrega el evento en la misma transacción. Las tablas `estado_bulto` y `cambio_estado_bulto` almacenan el resultado, pero no sustituyen al patrón.

**Strategy:** `PriceCalculator` recibe una `PricingPolicy`. `ListPrice` y `TenPercentDiscount` calculan el descuento unitario. La política se elige al iniciar una venta; el detalle guarda precio, descuento monetario y costo histórico. No hace falta persistir el nombre de la estrategia para reconstruir el importe cobrado.

**Repositorio / DAO y unidad de trabajo:** la aplicación usa los contratos de `domain/ports.py`; la infraestructura los implementa con SQLAlchemy. El repositorio entrega registros simples y mantiene los objetos ORM dentro de infraestructura. La unidad de trabajo gobierna confirmación, reversión y cierre.

## Correspondencia con las entidades

| Área | Tablas del DER |
| --- | --- |
| Ubicación | provincia, ciudad, domicilio |
| Maestros | establecimiento, categoria, proveedor, producto |
| Inventario | existencia |
| Compras | estado_compra, compra, detalle_compra |
| Reposición | estado_reposicion, orden_reposicion, detalle_reposicion |
| Remitos y bultos | estado_remito, remito, estado_precinto, estado_bulto, bulto, detalle_bulto, cambio_estado_bulto |
| Ventas y devoluciones | metodo_pago, venta, detalle_venta, motivo, devolucion, detalle_devolucion |

Las restricciones agregadas al diagrama, las unidades monetarias y las políticas de devolución o rechazo se explican en `reglas_inventadas_o_asumidas.md`. No se agregaron tablas de solicitudes, pagos, eventos alternativos ni movimientos.

## Extensiones y límites

Los estados de remito y orden se derivan, no se modifican desde el frontend. Los movimientos se reconstruyen mediante consultas sobre las operaciones existentes. El margen es bruto estimado, con costo histórico, y la valorización actual usa el costo de referencia.

No hay autenticación, usuarios, integración fiscal o bancaria. Se ejecuta en la máquina del grupo; no se presenta como un despliegue de producción. Se mantienen desactivaciones lógicas solo donde el DER contiene `esta_activo`. Las políticas de cancelación, daño y resolución de cuarentena no se inventan como operaciones adicionales.

## Referencias técnicas

- [FastAPI: aplicaciones con varios módulos](https://fastapi.tiangolo.com/tutorial/bigger-applications/).
- [FastAPI: pruebas](https://fastapi.tiangolo.com/tutorial/testing/).
- [Vite: guía de inicio](https://vite.dev/guide/).
- Bibliografía de la cátedra: semana 08 (SQLite, DAO y SQLAlchemy), semana 09 (State y Strategy) y semana 05 (abstracción y pruebas).
