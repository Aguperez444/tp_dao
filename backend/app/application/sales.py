from datetime import datetime, timezone, timedelta
from app.domain.errors import BusinessError
from app.domain.money import to_cents
from app.domain.pricing import PriceCalculator, policy_for
from .common import Service, now


class SalesService(Service):
    def _quote(self, r, data):
        self.local(r, data['local_id'])
        calculator = PriceCalculator(policy_for(data['politica']))
        lines = self.lines(r, data['detalles'])
        details = []
        for product_id, quantity in lines.items():
            product = self.require(r,'producto',product_id)
            stocks = r.list('existencia', establecimiento_id=data['local_id'], producto_id=product_id)
            available = stocks[0]['almacenado_total']-stocks[0]['reservado'] if stocks else 0
            if available < quantity:
                raise BusinessError(f'Stock disponible insuficiente para {product["nombre"]}: hay {available}.')
            price, discount = calculator.calculate(product['precio'])
            details.append(dict(producto_id=product_id, cantidad=quantity, precio_unitario=price, descuento_aplicado=discount, costo_unitario=product['costo_referencia']))
        total = sum(l['cantidad']*(l['precio_unitario']-l['descuento_aplicado']) for l in details)
        if total > 99_999_999_999:
            raise BusinessError('El total supera el máximo admitido de $999.999.999,99 por venta.')
        return {'detalles': details, 'total': total}

    def quote(self, data):
        with self.uow() as u:
            return self._quote(u.repo, data)

    def create(self, data):
        with self.uow(write=True) as u:
            r = u.repo
            self.require(r,'metodo_pago',data['metodo_pago_id'])
            quote = self._quote(r,data)
            if to_cents(data['importe_cobrado']) != quote['total']:
                raise BusinessError(f'El cobro debe coincidir con el total vigente: ${quote["total"]/100:.2f}. Revise los precios antes de confirmar.')
            sale = r.create('venta', dict(local_id=data['local_id'], metodo_pago_id=data['metodo_pago_id'], total=quote['total'], fecha=now(), numero_comprobante='V-PROVISIONAL'))
            r.update('venta',sale['id'],{'numero_comprobante': f'V-{sale["id"]:08d}'})
            for line in quote['detalles']:
                r.create('detalle_venta', {**line, 'venta_id': sale['id']})
                stock = r.stock(data['local_id'],line['producto_id'])
                r.update('existencia',stock['id'],{'almacenado_total': stock['almacenado_total']-line['cantidad']})
            return self._detail(r,sale['id'])

    def refund(self, id, data):
        if data.get('productos_aptos') is not True:
            raise BusinessError('Esta devolución requiere productos inspeccionados y aptos para reventa.')
        with self.uow(write=True) as u:
            r = u.repo
            sale = self.require(r,'venta',id)
            if datetime.now(timezone.utc) - datetime.fromisoformat(sale['fecha']) > timedelta(days=30):
                raise BusinessError('La venta superó el plazo de devolución de 30 días.')
            self.require(r,'motivo',data['motivo_id'])
            self.require(r,'metodo_pago',data['metodo_reintegro_id'])
            original = {line['producto_id']: line for line in r.list('detalle_venta', venta_id=id)}
            if not data['detalles']:
                raise BusinessError('Seleccione productos a devolver.')
            checked, seen = [], set()
            for line in data['detalles']:
                product, quantity = line['producto_id'], line['cantidad']
                if type(quantity) is not int or quantity <= 0 or product in seen:
                    raise BusinessError('Use cantidades enteras positivas y no repita productos.')
                seen.add(product)
                if product not in original or r.returned(id,product)+quantity > original[product]['cantidad']:
                    raise BusinessError('La devolución no corresponde a la venta o supera la cantidad pendiente.')
                unit = original[product]['precio_unitario']-original[product]['descuento_aplicado']
                checked.append(dict(producto_id=product,cantidad=quantity,importe_unitario=unit))
            refund = r.create('devolucion', dict(venta_id=id,motivo_id=data['motivo_id'],metodo_reintegro_id=data['metodo_reintegro_id'],detalle=data['detalle'].strip(),fecha=now()))
            for line in checked:
                r.create('detalle_devolucion', {**line,'devolucion_id':refund['id']})
                stock = r.stock(sale['local_id'],line['producto_id'])
                r.update('existencia',stock['id'],{'almacenado_total':stock['almacenado_total']+line['cantidad']})
            return self._detail(r,id)

    def _detail(self, r, id):
        sale = self.require(r,'venta',id)
        details = [{**line, 'producto':self.require(r,'producto',line['producto_id'],active=False)['nombre'], 'devuelta':r.returned(id,line['producto_id']), 'subtotal':line['cantidad']*(line['precio_unitario']-line['descuento_aplicado'])} for line in r.list('detalle_venta',venta_id=id)]
        refunds = []
        for refund in r.list('devolucion',venta_id=id):
            lines = r.list('detalle_devolucion',devolucion_id=refund['id'])
            refunds.append({**refund, 'numero_comprobante':f'D-{refund["id"]:08d}', 'motivo':self.require(r,'motivo',refund['motivo_id'])['nombre'], 'metodo_reintegro':self.require(r,'metodo_pago',refund['metodo_reintegro_id'])['nombre'], 'total':sum(l['cantidad']*l['importe_unitario'] for l in lines), 'detalles':lines})
        return {**sale,'local':self.require(r,'establecimiento',sale['local_id'])['nombre'], 'metodo_pago':self.require(r,'metodo_pago',sale['metodo_pago_id'])['nombre'], 'detalles':details, 'devoluciones':refunds, 'reintegrado':sum(refund['total'] for refund in refunds)}

    def get(self,id):
        with self.uow() as u:
            return self._detail(u.repo,id)

    def list(self):
        with self.uow() as u:
            r = u.repo
            return [{**sale,'local':self.require(r,'establecimiento',sale['local_id'])['nombre'], 'metodo_pago':self.require(r,'metodo_pago',sale['metodo_pago_id'])['nombre'], 'reintegrado':sum(line['cantidad']*line['importe_unitario'] for refund in r.list('devolucion',venta_id=sale['id']) for line in r.list('detalle_devolucion',devolucion_id=refund['id']))} for sale in r.list('venta')][::-1]
