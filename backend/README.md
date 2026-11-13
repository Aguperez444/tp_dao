# Backend de Nexo

La organización sigue las convenciones de `example/Ganker/backend`: módulos en
`snake_case`, clases en `PascalCase`, una clase por archivo, puertos con prefijo
`I`, implementaciones de repositorio con sufijo `Impl` y modelos SQLAlchemy con
sufijo `ORM`.

```text
app/
  application/
    dto/
      commands/                entradas tipadas de los casos de uso
      response/                resultados y proyecciones de consulta tipados
    ports/                     contratos de repositorio y unidad de trabajo
    services/                  coordinación compartida de logística y consultas
    use_cases/                 una operación por clase, con método execute
  domain/
    exceptions/                errores de negocio
    models/                    entidades Python independientes del ORM
    services/
      pricing/                 Strategy: políticas y cálculo de precios
      shipping/                State: estados y transiciones de bultos
                               validaciones, importes y períodos de consulta
  infrastructure/
    api/
      controllers/             rutas agrupadas por área funcional
      dependencies/            composición de dependencias HTTP
      dto/request/             un esquema de entrada por archivo
      middleware/              control del origen de las escrituras
    config/                    ruta de la base y orígenes locales
    database/
      base.py                  base declarativa de SQLAlchemy
      database.py              motor, sesiones e inicialización
      lookup_data.py           estados y referencias iniciales
      mappers/                 un mapper ORM ↔ dominio por entidad
      models/                  un modelo ORM por tabla
      repositories/            implementaciones de los puertos
      unit_of_work/            límites de transacción y fábrica
      seed_data.py             demostración en una única transacción
    start/main.py              composición de FastAPI
  main.py                      entrada compatible para Uvicorn
  seed.py                      entrada compatible para la demo por consola
```

Los controladores validan entradas mediante DTOs Pydantic y las convierten en
comandos de aplicación con `to_command()`. Los casos de uso reciben esos
comandos y devuelven DTOs de respuesta; las cantidades y los importes tienen
tipos explícitos. Las implementaciones SQLAlchemy quedan en
`infrastructure/database`; el dominio y los casos de uso no importan FastAPI,
Pydantic ni SQLAlchemy.

Hay 27 entidades de dominio y 27 mappers específicos, con métodos tipados
`orm_to_domain()` y `domain_to_orm()`. Por ejemplo, `ProductoMapper` convierte
`ProductoORM` en `Producto` y viceversa. Las entidades tienen identidad y
atributos propios; no contienen objetos de sesión ni métodos de acceso como
los de un diccionario.

`IEntityRepository[T]` define las operaciones comunes de repositorios tipados.
Cada implementación selecciona su modelo ORM y su mapper; los puertos
especializados agregan las consultas de stock y cantidades devueltas.
`IUnitOfWork` expone repositorios concretos por entidad, como `producto_repo`,
`venta_repo` y `existencia_repo`. Modificar una entidad de dominio solo se
persiste al invocar `update(entity)`. Los catálogos tienen casos de uso separados
por recurso y comparten las validaciones de normalización y unicidad.

`IReportsRepository` devuelve proyecciones tipadas. Las filas SQL se convierten
en DTOs dentro del repositorio, sin introducir SQL en los casos de uso. Los
diccionarios de negocio restantes representan índices por producto o cantidades
acumuladas, no entidades ni contratos de entrada o salida.

Los controladores usan prefijos por recurso: `/api/catalogos`, `/api/compras`,
`/api/reposiciones`, `/api/remitos`, `/api/bultos`, `/api/ventas`,
`/api/inventario` y `/api/reportes`. Las rutas públicas completas son las mismas.
Los DTOs de salida se serializan conservando el contrato y el OpenAPI anteriores.

Cada ejecución solicita una unidad de trabajo nueva. Las escrituras mantienen
`BEGIN IMMEDIATE`, commit al terminar y rollback ante errores. La carga de la
demo comparte una unidad de trabajo externa: sus operaciones se confirman o se
deshacen juntas.

## Ejecutar

Desde `backend/`, con las dependencias de `requirements.txt` instaladas:

```sh
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python -m app.seed
```

También se puede usar `app.infrastructure.start.main:app`. Se conservan
`NEXO_DB_PATH`, la ubicación predeterminada `backend/data/nexo.sqlite3`, las rutas
`/api`, los códigos HTTP, los mensajes de error y la conversión de pesos de
entrada a centavos de salida. La base existente no requiere migraciones.

## Verificación

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -t . -v
```

Las pruebas originales de negocio, API y concurrencia conservan sus escenarios
y resultados esperados. Los fixtures invocan los nuevos casos de uso con
comandos tipados y las pruebas de negocio consultan atributos de los DTOs.

`tests/test_compatibility.py` compara el OpenAPI completo y un escenario HTTP
contra resultados capturados **antes** de la refactorización. El escenario
incluye la demo, las altas y modificaciones de los ocho catálogos, ventas con
descuento, devoluciones, inventario, consultas, errores y el esquema SQLite
completo, incluidos índices y triggers. Solo se normalizan las marcas de tiempo
y la fecha final predeterminada de los reportes. Todas las bases de prueba son
temporales.

`tests/test_domain_persistence.py` verifica que las entidades se usen fuera de
la sesión, que sus cambios requieran persistencia explícita, que los mappers
conserven identidades y valores nulos, cero y falsos, y que un fallo tardío de
la demo revierta todos sus casos de uso.
