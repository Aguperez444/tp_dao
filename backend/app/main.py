from app.infrastructure.config.settings import DEFAULT_DB
from app.infrastructure.start.main import app, create_app

"Entrada compatible con uvicorn app.main:app."
__all__ = ["app", "create_app", "DEFAULT_DB"]
