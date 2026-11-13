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

## Estructura

```text
backend/
  app/
    application/     dto/, ports/, use_cases/ y services/
    domain/          models/, services/ y exceptions/; State y Strategy
    infrastructure/
      api/           controllers/, dto/, dependencies/ y middleware/
      database/      models/, mappers/, repositories/ y unit_of_work/
      config/        ruta de la base y orígenes locales
      start/main.py  composición de la aplicación
    main.py          entrada compatible para Uvicorn
    seed.py          entrada compatible para la demostración
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

El backend sigue las convenciones de `example/Ganker`: una clase por archivo,
puertos `I...`, repositorios `...Impl`, modelos `...ORM` y casos de uso con
`execute()`. Las entidades de dominio son clases Python independientes del ORM;
cada entidad tiene un mapper en ambos sentidos. Los casos de uso intercambian
comandos y respuestas tipadas. La organización y las pruebas de compatibilidad se detallan en
[backend/README.md](backend/README.md).

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

