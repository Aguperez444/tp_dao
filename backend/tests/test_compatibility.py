"""Contratos capturados del backend anterior a la reorganización."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase

from app.main import DEFAULT_DB, create_app

from tests.contract_capture import capture

FIXTURES = Path(__file__).parent / "fixtures"


class CompatibilityTests(IsolatedAsyncioTestCase):
    async def test_http_behavior_and_sqlite_schema_match_original_backend(self):
        expected = json.loads((FIXTURES / "backend_contract.json").read_text())
        self.assertEqual(await capture(), expected)

    def test_openapi_matches_original_backend(self):
        with TemporaryDirectory() as directory:
            app = create_app(Path(directory) / "openapi.sqlite3")
            self.addCleanup(app.state.database.dispose)
            expected = json.loads((FIXTURES / "openapi.json").read_text())
            self.assertEqual(app.openapi(), expected)

    def test_legacy_entrypoint_keeps_default_database_location(self):
        expected = Path(__file__).resolve().parents[1] / "data" / "nexo.sqlite3"
        self.assertEqual(DEFAULT_DB.resolve(), expected)
