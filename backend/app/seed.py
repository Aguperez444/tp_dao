import os

from app.infrastructure.database.seed_data import seed

"Entrada compatible: python -m app.seed."


def main() -> None:
    from app.infrastructure.config.settings import DEFAULT_DB
    from app.infrastructure.database.database import Database

    database = Database(os.environ.get("NEXO_DB_PATH", DEFAULT_DB))
    try:
        database.initialize()
        seed(database)
        print("Demo cargada correctamente en", database.path)
    finally:
        database.dispose()


if __name__ == "__main__":
    main()
