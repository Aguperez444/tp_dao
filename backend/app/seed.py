"""Ejemplos ficticios del circuito. Se rechaza cargar sobre una base con datos de negocio."""
import os
from app.application.catalog import CatalogService
from app.application.purchasing import PurchasingService
from app.application.logistics import LogisticsService
from app.application.sales import SalesService
from app.domain.errors import BusinessError


def seed(database):
    with database.uow(write=True) as u:
        if any(u.repo.list(table) for table in ('establecimiento','producto','proveedor','provincia','categoria','compra','venta')):
            raise BusinessError('La demo solo se puede cargar en una base vacía; sus datos actuales se conservan.')
    # Toda la carga, incluidos los servicios, comparte una única transacción.
    with database.uow(write=True) as root:
        class Nested:
            def __enter__(self):
                return root
            def __exit__(self,*args):
                return False
        factory = lambda **kwargs: Nested()
        catalog,purchasing,logistics,sales = CatalogService(factory),PurchasingService(factory),LogisticsService(factory),SalesService(factory)
        # Revalidar dentro del bloqueo de escritura evita dos cargas concurrentes.
        if root.repo.list('establecimiento') or root.repo.list('producto') or root.repo.list('provincia'):
            raise BusinessError('La base ya contiene datos.')
        province = catalog.save('provincia',{'nombre':'Córdoba'})['id']
        city = catalog.save('ciudad',{'nombre':'Córdoba','provincia_id':province})['id']
        establishments=[]
        for name,street,height,central in [('Centro de distribución','Av. Circunvalación','1200',True),('Local Centro','San Martín','245',False),('Local Norte','Av. Rafael Núñez','4100',False)]:
            address=catalog.save('domicilio',{'calle':street,'altura':height,'ciudad_id':city})['id']
            establishments.append(catalog.save('establecimiento',{'nombre':name,'es_central':central,'domicilio_id':address})['id'])
        cd,center,north=establishments
        category=catalog.save('categoria',{'nombre':'Almacén'})['id']
        supplier=catalog.save('proveedor',{'nombre':'Distribuidora de ejemplo','CUIT':'30-00000000-0','esta_activo':True})['id']
        products=[]
        for code,name,price,cost in [('YER-001','Yerba mate 1 kg','6500','4000'),('CAF-001','Café molido 250 g','4800','2900'),('AZU-001','Azúcar 1 kg','1800','1000')]:
            products.append(catalog.save('producto',{'codigo':code,'nombre':name,'detalle':'Producto de demostración','categoria_id':category,'precio':price,'costo_referencia':cost,'esta_activo':True})['id'])
        purchase=purchasing.create({'proveedor_id':supplier,'detalles':[dict(producto_id=p,cantidad=100,costo=c) for p,c in zip(products,['4000','2900','1000'])]})
        purchasing.receive(purchase['id'])
        for establishment in establishments:
            for product in products:
                catalog.minimum(establishment,product,10)
        order=logistics.create_order(dict(establecimiento_solicitante_id=center,establecimiento_proveedor_id=cd,detalles=[dict(producto_id=p,cantidad=q) for p,q in zip(products,[20,15,30])]))
        delivery=logistics.create_delivery(order['id'],'R-DEMO-001')
        packages=[]
        for lines in [[dict(producto_id=products[0],cantidad=20),dict(producto_id=products[1],cantidad=15)],[dict(producto_id=products[2],cantidad=30)]]:
            packages.append(logistics.prepare(delivery['id'],{'responsable':'Ana Demo','detalles':lines}))
        for i,package in enumerate(packages,1):
            logistics.transition(package['id'],'precintar',dict(responsable='Ana Demo',codigo_precinto=f'P-DEMO-{i}'))
        for i,package in enumerate(packages,1):
            logistics.transition(package['id'],'despachar',dict(responsable='Ana Demo'))
            logistics.transition(package['id'],'recibir',dict(responsable='Luis Demo'))
            logistics.transition(package['id'],'inspeccionar',dict(responsable='Luis Demo',codigo_precinto=f'P-DEMO-{i}',numero_remito='R-DEMO-001',precinto_intacto=True,contenido_conforme=True))
        sale=sales.create(dict(local_id=center,metodo_pago_id=root.repo.list('metodo_pago')[0]['id'],politica='lista',importe_cobrado='29100',detalles=[dict(producto_id=products[0],cantidad=3),dict(producto_id=products[1],cantidad=2)]))
        sales.refund(sale['id'],dict(motivo_id=root.repo.list('motivo')[0]['id'],metodo_reintegro_id=root.repo.list('metodo_pago')[0]['id'],detalle='Ejemplo de devolución parcial apta para reventa.',productos_aptos=True,detalles=[dict(producto_id=products[0],cantidad=1)]))
        order2=logistics.create_order(dict(establecimiento_solicitante_id=north,establecimiento_proveedor_id=cd,detalles=[dict(producto_id=products[0],cantidad=8)]))
        delivery2=logistics.create_delivery(order2['id'],'R-DEMO-002')
        package=logistics.prepare(delivery2['id'],dict(responsable='Ana Demo',detalles=[dict(producto_id=products[0],cantidad=8)]))
        logistics.transition(package['id'],'precintar',dict(responsable='Ana Demo',codigo_precinto='P-DEMO-3'))
        logistics.transition(package['id'],'despachar',dict(responsable='Ana Demo'))
        logistics.transition(package['id'],'recibir',dict(responsable='Luis Demo'))
        logistics.transition(package['id'],'inspeccionar',dict(responsable='Luis Demo',codigo_precinto='P-DEMO-3',numero_remito='R-DEMO-002',precinto_intacto=False,contenido_conforme=True,observacion='Precinto roto al recibir (ejemplo).'))


def main():
    from app.infrastructure.database import Database
    from app.main import DEFAULT_DB
    database=Database(os.environ.get('NEXO_DB_PATH',DEFAULT_DB))
    try:
        database.initialize()
        seed(database)
        print('Demo cargada correctamente en',database.path)
    finally:
        database.dispose()


if __name__=='__main__':
    main()
