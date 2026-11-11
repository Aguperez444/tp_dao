from app.domain.errors import BusinessError
from app.domain.shipping import Package, STATES
from .common import Service, now


class LogisticsService(Service):
    def create_order(self, data):
        with self.uow(write=True) as u:
            r = u.repo
            self.local(r, data['establecimiento_solicitante_id'])
            self.local(r, data['establecimiento_proveedor_id'], central=True)
            lines = self.lines(r, data['detalles'])
            order = r.create('orden_reposicion', dict(establecimiento_solicitante_id=data['establecimiento_solicitante_id'], establecimiento_proveedor_id=data['establecimiento_proveedor_id'], fecha=now(), estado_id=self.state_id(r,'estado_reposicion','Pendiente')))
            for product, quantity in lines.items():
                r.create('detalle_reposicion', dict(orden_id=order['id'], producto_id=product, cantidad=quantity))
            return order

    def create_delivery(self, order_id, number):
        number = number.strip().upper()
        if not number:
            raise BusinessError('Indique el número del remito.')
        with self.uow(write=True) as u:
            r = u.repo
            self.require(r, 'orden_reposicion', order_id)
            if any(self.state_name(r,'estado_remito',delivery['estado_remito_id']) == 'Pendiente' for delivery in r.list('remito',orden_reposicion_id=order_id)):
                raise BusinessError('Complete la preparación e inicie el despacho del remito pendiente antes de generar otro.')
            requested = {x['producto_id']: x['cantidad'] for x in r.list('detalle_reposicion', orden_id=order_id)}
            allocated = self.allocated(r, order_id)
            if all(allocated.get(p,0) >= q for p,q in requested.items()):
                raise BusinessError('La orden ya tiene toda la mercadería asignada a bultos.')
            return r.create('remito', dict(orden_reposicion_id=order_id, numero_remito=number, fecha_emision=now(), estado_remito_id=self.state_id(r,'estado_remito','Pendiente')))

    def allocated(self, r, order_id):
        quantities = {}
        for delivery in r.list('remito', orden_reposicion_id=order_id):
            for package in r.list('bulto', remito_id=delivery['id']):
                for line in r.list('detalle_bulto', bulto_id=package['id']):
                    p = line['producto_id']
                    quantities[p] = quantities.get(p,0) + line['cantidad']
        return quantities

    def prepare(self, delivery_id, data):
        with self.uow(write=True) as u:
            r = u.repo
            delivery = self.require(r, 'remito', delivery_id)
            if self.state_name(r, 'estado_remito', delivery['estado_remito_id']) != 'Pendiente':
                raise BusinessError('El remito ya inició su despacho y no admite más bultos.')
            order = self.require(r, 'orden_reposicion', delivery['orden_reposicion_id'])
            requested = {x['producto_id']: x['cantidad'] for x in r.list('detalle_reposicion', orden_id=order['id'])}
            allocated = self.allocated(r, order['id'])
            lines = self.lines(r, data['detalles'])
            for p,q in lines.items():
                if allocated.get(p,0)+q > requested.get(p,0):
                    raise BusinessError('El bulto excede lo solicitado o incluye un producto ajeno a la orden.')
                stock = r.stock(order['establecimiento_proveedor_id'], p)
                if stock['almacenado_total']-stock['reservado'] < q:
                    raise BusinessError('No hay stock disponible suficiente en el CD.')
                r.update('existencia', stock['id'], {'reservado': stock['reservado']+q})
            package = r.create('bulto', dict(remito_id=delivery_id, estado_precinto_id=self.state_id(r,'estado_precinto','Sin colocar'), estado_bulto_id=self.state_id(r,'estado_bulto','Preparado'), codigo_precinto=None))
            for p,q in lines.items():
                r.create('detalle_bulto', dict(bulto_id=package['id'], producto_id=p, cantidad=q))
            self.event(r, package['id'], 'Preparado', data['responsable'], 'Mercadería reservada en el CD.')
            self.refresh_order(r, order['id'])
            return package

    def event(self, r, id, state, responsible, note):
        responsible = responsible.strip()
        if not responsible:
            raise BusinessError('Identifique al responsable de la operación.')
        r.create('cambio_estado_bulto', dict(bulto_id=id, estado_bulto_id=self.state_id(r,'estado_bulto',state), fecha=now(), responsable=responsible, observacion=note))

    def transition(self, id, action, data):
        with self.uow(write=True) as u:
            r = u.repo
            package = self.require(r, 'bulto', id)
            delivery = self.require(r,'remito',package['remito_id'])
            order = self.require(r,'orden_reposicion',delivery['orden_reposicion_id'])
            state_name = self.state_name(r,'estado_bulto',package['estado_bulto_id'])
            note = data.get('observacion','').strip()
            changes = {}
            if action == 'inspeccionar':
                seal = data.get('codigo_precinto','').strip().upper()
                same_seal = seal == package['codigo_precinto']
                same_delivery = data.get('numero_remito','').strip().upper() == delivery['numero_remito']
                intact = data.get('precinto_intacto') is True
                conforming = data.get('contenido_conforme') is True
                valid = same_seal and same_delivery and intact and conforming
                action = 'verificar' if valid else 'rechazar'
                if not valid and not note:
                    raise BusinessError('Explique el motivo del rechazo.')
                seal_state = 'Violado' if not intact else ('No coincide' if not same_seal else 'Intacto')
                changes['estado_precinto_id'] = self.state_id(r,'estado_precinto',seal_state)
            elif action in ('verificar','rechazar'):
                raise BusinessError('El resultado se obtiene inspeccionando el precinto y el remito.')
            new_state = Package(STATES[state_name]()).execute(action)
            if action == 'precintar':
                seal = data.get('codigo_precinto','').strip().upper()
                if not seal:
                    raise BusinessError('Debe registrar un código de precinto único.')
                changes.update(codigo_precinto=seal, estado_precinto_id=self.state_id(r,'estado_precinto','Intacto'))
            if action == 'despachar':
                packages = r.list('bulto', remito_id=delivery['id'])
                if any(self.state_name(r,'estado_bulto',x['estado_bulto_id']) == 'Preparado' for x in packages):
                    raise BusinessError('Precinte todos los bultos del remito antes del primer despacho.')
                for line in r.list('detalle_bulto', bulto_id=id):
                    stock = r.stock(order['establecimiento_proveedor_id'], line['producto_id'])
                    r.update('existencia', stock['id'], {'almacenado_total': stock['almacenado_total']-line['cantidad'], 'reservado': stock['reservado']-line['cantidad']})
            changes['estado_bulto_id'] = self.state_id(r,'estado_bulto',new_state)
            r.update('bulto', id, changes)
            self.event(r, id, new_state, data['responsable'], note or action.capitalize())
            self.refresh_delivery(r, delivery)
            self.refresh_order(r, order['id'])
            return {**self.require(r,'bulto',id), 'estado': new_state}

    def refresh_delivery(self, r, delivery):
        packages = r.list('bulto', remito_id=delivery['id'])
        states = [self.state_name(r,'estado_bulto',p['estado_bulto_id']) for p in packages]
        old_state = self.state_name(r,'estado_remito',delivery['estado_remito_id'])
        if old_state in ('Verificado', 'Rechazado'):
            return
        if 'Rechazado' in states:
            new_state = 'Rechazado'
        elif all(s == 'Verificado' for s in states):
            new_state = 'Verificado'
            order = self.require(r,'orden_reposicion',delivery['orden_reposicion_id'])
            for package in packages:
                for line in r.list('detalle_bulto', bulto_id=package['id']):
                    stock = r.stock(order['establecimiento_solicitante_id'], line['producto_id'])
                    r.update('existencia', stock['id'], {'almacenado_total': stock['almacenado_total']+line['cantidad']})
        elif all(s in ('Recibido','Verificado') for s in states):
            new_state = 'Recibido'
        elif any(s in ('En tránsito','Recibido','Verificado') for s in states):
            new_state = 'En tránsito'
        else:
            new_state = 'Pendiente'
        r.update('remito', delivery['id'], {'estado_remito_id': self.state_id(r,'estado_remito',new_state)})

    def refresh_order(self, r, id):
        deliveries = r.list('remito', orden_reposicion_id=id)
        states = [self.state_name(r,'estado_remito',d['estado_remito_id']) for d in deliveries]
        allocated = self.allocated(r, id)
        all_allocated = all(allocated.get(x['producto_id'],0) == x['cantidad'] for x in r.list('detalle_reposicion', orden_id=id))
        if all_allocated and states and all(s == 'Verificado' for s in states):
            state = 'Completada'
        elif 'Rechazado' in states:
            state = 'Con rechazos'
        elif any(s in ('En tránsito','Recibido','Verificado') for s in states):
            state = 'En tránsito'
        elif allocated:
            state = 'En preparación'
        else:
            state = 'Pendiente'
        r.update('orden_reposicion', id, {'estado_id': self.state_id(r,'estado_reposicion',state)})

    def list_orders(self):
        with self.uow() as u:
            r = u.repo
            rows = []
            for order in r.list('orden_reposicion'):
                lines = r.list('detalle_reposicion', orden_id=order['id'])
                allocated = self.allocated(r, order['id'])
                deliveries = []
                for delivery in r.list('remito', orden_reposicion_id=order['id']):
                    packages = []
                    for package in r.list('bulto', remito_id=delivery['id']):
                        history = [{**ev, 'estado': self.state_name(r,'estado_bulto',ev['estado_bulto_id'])} for ev in r.list('cambio_estado_bulto', bulto_id=package['id'])]
                        packages.append({**package, 'estado': self.state_name(r,'estado_bulto',package['estado_bulto_id']), 'estado_precinto': self.state_name(r,'estado_precinto',package['estado_precinto_id']), 'detalles': r.list('detalle_bulto', bulto_id=package['id']), 'historial': history})
                    deliveries.append({**delivery, 'estado': self.state_name(r,'estado_remito',delivery['estado_remito_id']), 'bultos': packages})
                rows.append({**order, 'origen': self.require(r,'establecimiento',order['establecimiento_proveedor_id'])['nombre'], 'destino': self.require(r,'establecimiento',order['establecimiento_solicitante_id'])['nombre'], 'estado': self.state_name(r,'estado_reposicion',order['estado_id']), 'detalles': [{**line, 'asignada': allocated.get(line['producto_id'],0)} for line in lines], 'remitos': deliveries})
            return rows[::-1]
