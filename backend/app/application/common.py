from datetime import datetime, timezone
from typing import Callable
from app.domain.errors import BusinessError, NotFoundError
from app.domain.ports import UnitOfWork


def now():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')


class Service:
    def __init__(self, uow_factory: Callable[..., UnitOfWork]):
        self.uow = uow_factory

    def require(self, repo, table, id, active=True):
        row = repo.get(table, id)
        if not row:
            raise NotFoundError(f'No existe {table} #{id}.')
        if active and row.get('esta_activo') is False:
            raise BusinessError(f'{table} #{id} está inactivo.')
        return row

    def state_id(self, repo, table, name):
        rows = repo.list(table, nombre=name)
        if not rows:
            raise BusinessError(f'Estado o referencia no configurado: {name}.')
        return rows[0]['id']

    def state_name(self, repo, table, id):
        return self.require(repo, table, id)['nombre']

    def local(self, repo, id, central=False):
        row = self.require(repo, 'establecimiento', id)
        if row['es_central'] != central:
            raise BusinessError('Se requiere un centro de distribución.' if central else 'Se requiere un local de venta.')
        return row

    def central(self, repo):
        rows = repo.list('establecimiento', es_central=True)
        if len(rows) != 1:
            raise BusinessError('Registre primero el único centro de distribución.')
        return rows[0]

    def lines(self, repo, lines):
        if not lines:
            raise BusinessError('La operación debe contener productos.')
        result = {}
        for item in lines:
            id, quantity = item['producto_id'], item['cantidad']
            if type(quantity) is not int or quantity <= 0:
                raise BusinessError('Las cantidades deben ser enteros positivos.')
            self.require(repo, 'producto', id)
            if id in result:
                raise BusinessError('Incluya cada producto una sola vez, consolidando sus cantidades.')
            result[id] = quantity
        return result
