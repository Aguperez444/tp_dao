from app.domain.errors import BusinessError
from app.domain.money import to_cents
from .common import Service

EDITABLE = {'categoria', 'provincia', 'ciudad', 'domicilio', 'establecimiento', 'proveedor', 'producto', 'motivo'}
READABLE = EDITABLE | {'estado_compra', 'estado_reposicion', 'estado_remito', 'estado_precinto', 'estado_bulto', 'metodo_pago'}


class CatalogService(Service):
    def list_all(self):
        with self.uow() as u:
            return {table: u.repo.list(table) for table in sorted(READABLE)}

    def save(self, table, data, id=None):
        if table not in EDITABLE:
            raise BusinessError('Este catálogo no admite edición.')
        values = dict(data)
        for key, value in values.items():
            if isinstance(value, str):
                values[key] = value.strip()
                if key not in ('detalle',) and not values[key]:
                    raise BusinessError('Complete los campos obligatorios.')
        with self.uow(write=True) as u:
            r = u.repo
            previous = self.require(r, table, id, active=False) if id else None
            if 'nombre' in values:
                # Comparación normalizada; el índice UNIQUE también protege carreras.
                for other in r.list(table):
                    if other['id'] != id and other.get('nombre','').casefold() == values['nombre'].casefold() and table not in ('producto','proveedor','domicilio'):
                        if table != 'ciudad' or other['provincia_id'] == values['provincia_id']:
                            raise BusinessError('Ya existe un registro con ese nombre.')
            if table == 'proveedor':
                values['CUIT'] = values['CUIT'].replace('-', '').replace(' ', '')
                if not values['CUIT'].isascii() or not values['CUIT'].isdigit() or len(values['CUIT']) != 11:
                    raise BusinessError('El CUIT debe contener 11 dígitos (se admiten guiones).')
            if table == 'producto':
                values['codigo'] = values['codigo'].upper()
                values['precio'] = to_cents(values['precio'])
                values['costo_referencia'] = to_cents(values['costo_referencia'])
                if values['precio'] <= 0:
                    raise BusinessError('El precio de venta debe ser mayor que cero.')
                self.require(r, 'categoria', values['categoria_id'])
            if table == 'ciudad':
                self.require(r, 'provincia', values['provincia_id'])
            if table == 'domicilio':
                self.require(r, 'ciudad', values['ciudad_id'])
            if table == 'establecimiento':
                self.require(r, 'domicilio', values['domicilio_id'])
                if previous and previous['es_central'] != values['es_central']:
                    raise BusinessError('No se puede convertir un local en CD ni un CD en local.')
                if values['es_central'] and any(x['id'] != id for x in r.list(table, es_central=True)):
                    raise BusinessError('Solo puede existir un centro de distribución.')
            return r.update(table, id, values) if id else r.create(table, values)

    def minimum(self, local, product, minimum):
        if type(minimum) is not int or minimum < 0:
            raise BusinessError('El mínimo debe ser un entero no negativo.')
        with self.uow(write=True) as u:
            self.require(u.repo, 'establecimiento', local)
            self.require(u.repo, 'producto', product)
            row = u.repo.stock(local, product)
            return u.repo.update('existencia', row['id'], {'minimo_permitido': minimum})
