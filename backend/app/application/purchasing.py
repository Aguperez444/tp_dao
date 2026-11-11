from app.domain.errors import BusinessError
from app.domain.money import to_cents
from .common import Service, now


class PurchasingService(Service):
    def create(self, data):
        with self.uow(write=True) as u:
            r = u.repo
            self.central(r)
            self.require(r, 'proveedor', data['proveedor_id'])
            self.lines(r, data['detalles'])
            purchase = r.create('compra', {'proveedor_id': data['proveedor_id'], 'estado_id': self.state_id(r,'estado_compra','Pendiente'), 'fecha': now()})
            for line in data['detalles']:
                r.create('detalle_compra', {'compra_id': purchase['id'], 'producto_id': line['producto_id'], 'cantidad': line['cantidad'], 'costo': to_cents(line['costo'])})
            return purchase

    def receive(self, id):
        with self.uow(write=True) as u:
            r = u.repo
            purchase = self.require(r, 'compra', id)
            if self.state_name(r,'estado_compra',purchase['estado_id']) != 'Pendiente':
                raise BusinessError('La compra ya fue recibida; no se puede acreditar nuevamente.')
            cd = self.central(r)
            for line in r.list('detalle_compra', compra_id=id):
                stock = r.stock(cd['id'], line['producto_id'])
                r.update('existencia', stock['id'], {'almacenado_total': stock['almacenado_total'] + line['cantidad']})
            return r.update('compra', id, {'estado_id': self.state_id(r,'estado_compra','Recibida'), 'fecha': now()})

    def list(self):
        with self.uow() as u:
            r = u.repo
            results = []
            for purchase in r.list('compra'):
                lines = r.list('detalle_compra', compra_id=purchase['id'])
                results.append({**purchase, 'estado': self.state_name(r,'estado_compra',purchase['estado_id']),
                    'proveedor': self.require(r,'proveedor',purchase['proveedor_id'],active=False)['nombre'],
                    'total': sum(x['cantidad'] * x['costo'] for x in lines), 'detalles': lines})
            return results[::-1]
