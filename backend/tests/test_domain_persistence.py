from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from app.domain.models.producto import Producto
from app.infrastructure.database.database import Database
from app.infrastructure.database.mappers.bulto_mapper import BultoMapper
from app.infrastructure.database.models.bulto_orm import BultoORM
from app.infrastructure.database.repositories.venta_repository_impl import (
    VentaRepositoryImpl,
)
from app.infrastructure.database.seed_data import seed

from tests.helpers import Fixture


class DomainPersistenceTests(TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.database = Database(Path(self.directory.name) / "domain.sqlite3")
        self.addCleanup(self.database.dispose)
        self.database.initialize()
        self.fixture = Fixture(self.database)

    def test_domain_changes_require_explicit_repository_update(self):
        with self.database.uow() as uow:
            product = uow.producto_repo.get(self.fixture.p)
        self.assertIsInstance(product, Producto)

        # La entidad sigue disponible fuera de la sesión y no escribe por sí sola.
        product.precio = 12345
        product.costo_referencia = 6789
        product.detalle = "Detalle conservado entre las dos representaciones."
        product.esta_activo = False
        with self.database.uow() as uow:
            persisted = uow.producto_repo.get(product.id)
            self.assertEqual(persisted.precio, 10000)
            self.assertTrue(persisted.esta_activo)

        with self.database.uow(write=True) as uow:
            saved = uow.producto_repo.update(product)
            self.assertIsInstance(saved, Producto)
            self.assertIsNot(saved, product)

        with self.database.uow() as uow:
            reloaded = uow.producto_repo.get(product.id)
        self.assertEqual(reloaded.precio, 12345)
        self.assertEqual(reloaded.costo_referencia, 6789)
        self.assertEqual(reloaded.detalle, product.detalle)
        self.assertFalse(reloaded.esta_activo)
        self.assertEqual(reloaded.codigo, "A")
        self.assertEqual(reloaded.categoria_id, self.fixture.category)

    def test_saving_new_domain_entity_assigns_identity_and_preserves_zero_and_false(
        self,
    ):
        product = Producto(
            codigo="NUEVO",
            nombre="Producto nuevo",
            categoria_id=self.fixture.category,
            precio=1050,
            costo_referencia=0,
            esta_activo=False,
        )
        self.assertFalse(product.is_persisted())
        with self.database.uow(write=True) as uow:
            saved = uow.producto_repo.save(product)
        self.assertTrue(saved.is_persisted())
        self.assertGreater(saved.id, 0)
        with self.database.uow() as uow:
            reloaded = uow.producto_repo.get(saved.id)
        self.assertEqual(reloaded.precio, 1050)
        self.assertEqual(reloaded.costo_referencia, 0)
        self.assertFalse(reloaded.esta_activo)
        self.assertEqual(reloaded.detalle, "")

    def test_package_mapper_preserves_absent_seal_and_identity(self):
        original = BultoORM(
            id=7,
            remito_id=8,
            estado_precinto_id=1,
            estado_bulto_id=2,
            codigo_precinto=None,
        )
        domain = BultoMapper.orm_to_domain(original)
        original.codigo_precinto = "SOLO-ORM"
        self.assertIsNone(domain.codigo_precinto)
        restored = BultoMapper.domain_to_orm(domain)
        self.assertEqual(restored.id, 7)
        self.assertEqual(restored.remito_id, 8)
        self.assertEqual(restored.estado_precinto_id, 1)
        self.assertEqual(restored.estado_bulto_id, 2)
        self.assertIsNone(restored.codigo_precinto)

    def test_demo_rolls_back_all_use_cases_if_a_late_operation_fails(self):
        database = Database(Path(self.directory.name) / "empty.sqlite3")
        self.addCleanup(database.dispose)
        database.initialize()
        with patch.object(
            VentaRepositoryImpl, "save", side_effect=RuntimeError("fallo")
        ):
            with self.assertRaisesRegex(RuntimeError, "fallo"):
                seed(database)
        with database.uow() as uow:
            self.assertEqual(uow.producto_repo.list(), [])
            self.assertEqual(uow.compra_repo.list(), [])
            self.assertEqual(uow.bulto_repo.list(), [])
            self.assertEqual(uow.cambio_estado_bulto_repo.list(), [])
        # El fallo también cierra la transacción y permite una nueva carga completa.
        seed(database)
        with database.uow() as uow:
            self.assertEqual(len(uow.venta_repo.list()), 1)
