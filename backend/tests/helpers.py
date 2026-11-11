from app.application.catalog import CatalogService
from app.application.purchasing import PurchasingService
from app.application.logistics import LogisticsService
from app.application.sales import SalesService
from app.infrastructure.reports import ReportsRepository


class Fixture:
    def __init__(self, database):
        self.db=database
        self.catalog=CatalogService(database.uow)
        self.purchasing=PurchasingService(database.uow)
        self.logistics=LogisticsService(database.uow)
        self.sales=SalesService(database.uow)
        self.reports=ReportsRepository(database)
        province=self.catalog.save('provincia',{'nombre':'Córdoba'})['id']
        city=self.catalog.save('ciudad',{'nombre':'Córdoba','provincia_id':province})['id']
        address=self.catalog.save('domicilio',{'calle':'Ejemplo','altura':'123','ciudad_id':city})['id']
        self.cd=self.catalog.save('establecimiento',dict(nombre='CD',es_central=True,domicilio_id=address))['id']
        self.local=self.catalog.save('establecimiento',dict(nombre='Centro',es_central=False,domicilio_id=address))['id']
        self.north=self.catalog.save('establecimiento',dict(nombre='Norte',es_central=False,domicilio_id=address))['id']
        self.category=self.catalog.save('categoria',{'nombre':'Almacén'})['id']
        self.supplier=self.catalog.save('proveedor',dict(nombre='Proveedor',CUIT='30-00000000-0',esta_activo=True))['id']
        self.p=self.catalog.save('producto',dict(codigo='A',nombre='Arroz',detalle='',categoria_id=self.category,precio='100',costo_referencia='60',esta_activo=True))['id']
        self.p2=self.catalog.save('producto',dict(codigo='B',nombre='Aceite',detalle='',categoria_id=self.category,precio='200',costo_referencia='120',esta_activo=True))['id']
        with database.uow() as u:
            self.method=u.repo.list('metodo_pago')[0]['id']
            self.reason=u.repo.list('motivo')[0]['id']
        self._counter=0

    def purchase(self, receive=True):
        p=self.purchasing.create(dict(proveedor_id=self.supplier,detalles=[dict(producto_id=self.p,cantidad=100,costo='60'),dict(producto_id=self.p2,cantidad=20,costo='120')]))
        if receive:self.purchasing.receive(p['id'])
        return p

    def order(self, quantity=10, second=0):
        details=[dict(producto_id=self.p,cantidad=quantity)]
        if second:details.append(dict(producto_id=self.p2,cantidad=second))
        return self.logistics.create_order(dict(establecimiento_solicitante_id=self.local,establecimiento_proveedor_id=self.cd,detalles=details))

    def delivery(self, order):
        self._counter+=1
        return self.logistics.create_delivery(order['id'],f'R-{self._counter}')

    def package(self, delivery, quantity=10, second=0):
        lines=[dict(producto_id=self.p,cantidad=quantity)]
        if second:lines.append(dict(producto_id=self.p2,cantidad=second))
        return self.logistics.prepare(delivery['id'],dict(responsable='Ana',detalles=lines))

    def seal(self, package):
        return self.logistics.transition(package['id'],'precintar',dict(responsable='Ana',codigo_precinto=f'S-{package["id"]}'))

    def receive(self, package):
        self.logistics.transition(package['id'],'despachar',dict(responsable='Ana'))
        self.logistics.transition(package['id'],'recibir',dict(responsable='Luis'))

    def verify(self, package, delivery, **extra):
        data=dict(responsable='Luis',codigo_precinto=f'S-{package["id"]}',numero_remito=delivery['numero_remito'],precinto_intacto=True,contenido_conforme=True)
        return self.logistics.transition(package['id'],'inspeccionar',{**data,**extra})

    def supply(self, quantity=10):
        self.purchase()
        order=self.order(quantity);delivery=self.delivery(order);package=self.package(delivery,quantity)
        self.seal(package);self.receive(package);self.verify(package,delivery)
        return package,delivery

    def stock(self, establishment, product=None):
        with self.db.uow() as u:
            rows=u.repo.list('existencia',establecimiento_id=establishment,producto_id=product or self.p)
            return (rows[0]['almacenado_total'],rows[0]['reservado']) if rows else (0,0)

    def sell(self, quantity=1, **extra):
        data=dict(local_id=self.local,metodo_pago_id=self.method,politica='lista',importe_cobrado=str(quantity*100),detalles=[dict(producto_id=self.p,cantidad=quantity)])
        return self.sales.create({**data,**extra})

    def refund(self,sale,quantity=1,**extra):
        data=dict(motivo_id=self.reason,metodo_reintegro_id=self.method,detalle='Cambio solicitado',productos_aptos=True,detalles=[dict(producto_id=self.p,cantidad=quantity)])
        return self.sales.refund(sale['id'],{**data,**extra})
