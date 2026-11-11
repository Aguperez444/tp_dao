# Nexo · Distribución y ventas

TP integrador de **Desarrollo de Aplicaciones con Objetos — 2026**, grupo 40, tema 3. Implementación basada en `der_5_tp_dao.jpg`, `Presentacion-grupo-40.docx`, `tema3.pdf` y los apuntes de `BILBIOGRAFIA/`.

Frontend **React + TypeScript + Vite**, backend **FastAPI con arquitectura por capas**, ORM **SQLAlchemy** y base **SQLite 3**. Python y frontend están separados; FastAPI entrega exclusivamente JSON.

## Requisitos

- Python **3.11 o superior** (verificado con 3.14).
- Node.js **22.12 o superior** y npm (verificado con 22.22).
- Internet para instalar dependencias si no están disponibles en caché.

## Iniciar el backend

En una terminal:

```sh
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

En Windows, activar con `.venv\Scripts\activate` y usar `py` si corresponde.

La base se crea automáticamente en `backend/data/nexo.sqlite3`. El motor es SQLite, sin servidor de base de datos adicional. La documentación interactiva está en **http://127.0.0.1:8000/docs** y el chequeo de salud en **http://127.0.0.1:8000/api/salud**.

La variable de entorno `NEXO_DB_PATH` permite elegir otra base; debe establecerse tanto al cargar la demo por consola como al ejecutar el servidor. No se carga un archivo `.env` automáticamente.

## Iniciar el frontend

En otra terminal, desde la raíz del proyecto:

```sh
cd frontend
npm ci
npm run dev
```

Abrir **http://127.0.0.1:5173**. Vite redirige `/api` al backend de `127.0.0.1:8000`; no hace falta editar URLs en el código. Si se cambia el puerto del backend, ajustar el proxy en `frontend/vite.config.ts`.

En la primera pantalla se puede usar **Cargar demostración**. La demo solo se carga en una base sin datos de negocio y nunca sobrescribe operaciones. También se puede ejecutar, con el servidor detenido y desde `backend/`:

```sh
python -m app.seed
```

La demo contiene un CD, dos locales, tres productos, una compra recibida, una reposición con dos bultos verificados, una venta de dos productos, una devolución parcial y un segundo remito rechazado por precinto roto.

## Recorrer el sistema

1. **Catálogo:** administrar productos, categorías, proveedores y establecimientos. Para crear una ubicación, elegir Provincias, Ciudades y Domicilios en el selector de otros catálogos, en ese orden. Crear el CD y después los locales. Producto/proveedor admiten desactivación.
2. **Compras:** registrar varios productos y sus costos. La compra queda Pendiente; abrirla y confirmar su recepción para ingresar stock al CD.
3. **Reposición y bultos:** cargar las necesidades consolidadas de un local, crear un remito y preparar sus bultos. La preparación reserva unidades del CD. Precintar todos los bultos de ese remito antes de iniciar su despacho. Una orden admite varios remitos para entregas parciales.
4. Registrar despacho y recepción física por separado. Inspeccionar número de remito, código e integridad del precinto y conformidad del contenido. Un rechazo requiere observación. El destino no tiene disponible hasta que todo el remito esté verificado.
5. **Ventas y devoluciones:** elegir local, productos, política de precios y un medio de pago. El importe cobrado debe coincidir con el total. Abrir el comprobante para imprimirlo o devolver unidades de la venta, con motivo, medio de reintegro y confirmación de aptitud para reventa.
6. **Inventario:** consultar disponible, reservado, mínimo y valorización; editar mínimos por producto/local y consultar los movimientos.
7. **Reportes:** consultar los cinco informes, con período inclusivo y establecimiento. Los filtros temporales usan UTC; las existencias muestran siempre la situación actual.

## Estructura

```text
backend/
  app/
    api/             rutas HTTP, validación y control de origen
    application/     casos de uso y coordinación transaccional
    domain/          State, Strategy, contratos y reglas monetarias
    infrastructure/  SQLAlchemy, repositorios, consultas y SQLite
    main.py          composición de la aplicación
    seed.py          demostración transaccional
  tests/             pruebas de negocio, concurrencia y contratos HTTP
  requirements.txt
  requirements-dev.txt
frontend/
  src/
    components/      controles compartidos
    pages/           pantallas por operación
    api.ts           cliente HTTP y formatos
    state.tsx        carga de datos y estado de solicitudes
  package.json
  package-lock.json
  vite.config.ts
docs/
reglas_inventadas_o_asumidas.md
```

- [Reglas asumidas y justificaciones](reglas_inventadas_o_asumidas.md).
- [Arquitectura y correspondencia con el DER](docs/arquitectura.md).
- [Cumplimiento y criterios de prueba](docs/cumplimiento.md).

Los importes de entrada en la API se expresan en pesos; los importes devueltos y persistidos son **centavos enteros**. El frontend presenta pesos. `detalle_venta` conserva precio, descuento monetario unitario y costo al momento de la venta. Las escrituras usan `BEGIN IMMEDIATE`, claves foráneas y restricciones de integridad.

## Pruebas y compilación

Desde `backend/`, con el entorno virtual activado:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -t . -v
```

No hace falta pytest. Las bases de prueba son temporales y no alteran la aplicación. Se verifican sobreventa concurrente, doble acreditación, reservas, rechazo de sellos, devoluciones concurrentes, costo histórico, filtros, contratos HTTP y conciliación del inventario.

Desde `frontend/`:

```sh
npm run build
npm run preview
```

`build` valida TypeScript y genera `frontend/dist/`. `preview` sirve ese build en **http://127.0.0.1:4173**, con el mismo proxy hacia FastAPI; el backend debe seguir encendido. El frontend no está servido desde FastAPI.

## Base anterior y limpieza

El prototipo anterior y sus documentos generados quedaron reemplazados. Se conservaron los PDF, la presentación del grupo y el DER del usuario. La base anterior se respaldó con la API de backup de SQLite en `backend/backups/nexo-anterior.sqlite3`, fuera de la aplicación activa. No hay una migración automática: las entidades y varias reglas cambiaron para respetar el DER.

Para resguardar la base nueva, detener el backend y copiar `backend/data/nexo.sqlite3`. Para probar desde cero sin borrar datos, seleccionar otra ruta mediante `NEXO_DB_PATH`.

## Límites

Aplicación académica local, sin autenticación. El nombre del responsable es declarado por el operador. Las operaciones bancarias y fiscales se simulan; los comprobantes no tienen validez fiscal. El margen informado es bruto estimado, sin gastos ni impuestos.

No se incluyen pagos combinados, clientes frecuentes, lotes/vencimientos, cancelación de operaciones ni disposición posterior de rechazos. Solo se aceptan devoluciones aptas para reventa, porque el DER no representa aptitud o merma. Todas estas decisiones están justificadas en el documento de reglas asumidas.

La compilación del frontend y las pruebas de API/negocio se ejecutaron. La revisión visual en navegador y el arranque real de ambos servidores quedan limitados por la restricción de sockets del entorno de elaboración.
