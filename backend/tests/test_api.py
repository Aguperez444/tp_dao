"""Contratos HTTP reales mediante ASGITransport, sin abrir puertos.

Los endpoints son síncronos en producción. En estas pruebas se ejecutan inline
para no depender de notificaciones de sockets entre hilos en un sandbox.
La concurrencia de escrituras se prueba aparte con hilos reales.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
import httpx
from app.main import create_app
from tests.helpers import Fixture


async def inline(function,*args,**kwargs):
    return function(*args,**kwargs)


class ApiTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.app=create_app(Path(self.tmp.name)/'api.sqlite3')
        self.app.state.database.initialize();self.addCleanup(self.app.state.database.dispose)
        self.f=Fixture(self.app.state.database)
        for target in ('fastapi.routing.run_in_threadpool','starlette.routing.run_in_threadpool'):
            mock=patch(target,inline);mock.start();self.addCleanup(mock.stop)
        self.client=httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app),base_url='http://test')
        self.addAsyncCleanup(self.client.aclose)

    async def post(self,url,data=None,expected=201):
        result=await self.client.post('/api'+url,json=data or {})
        self.assertEqual(result.status_code,expected,result.text)
        return result.json()

    async def test_complete_api_flow(self):
        f=self.f
        purchase=await self.post('/compras',dict(proveedor_id=f.supplier,detalles=[dict(producto_id=f.p,cantidad=10,costo='60')]))
        await self.post(f'/compras/{purchase["id"]}/recepcion',expected=200)
        order=await self.post('/reposiciones',dict(establecimiento_solicitante_id=f.local,establecimiento_proveedor_id=f.cd,detalles=[dict(producto_id=f.p,cantidad=5)]))
        delivery=await self.post(f'/reposiciones/{order["id"]}/remitos',dict(numero_remito='R-API'))
        package=await self.post(f'/remitos/{delivery["id"]}/bultos',dict(responsable='Ana',detalles=[dict(producto_id=f.p,cantidad=5)]))
        for action,data in [('precintar',dict(codigo_precinto='S-API')),('despachar',{}),('recibir',{}),('inspeccionar',dict(codigo_precinto='S-API',numero_remito='R-API',precinto_intacto=True,contenido_conforme=True))]:
            await self.post(f'/bultos/{package["id"]}/{action}',dict(responsable='Ana',**data),expected=200)
        quote=await self.post('/ventas/cotizacion',dict(local_id=f.local,politica='lista',detalles=[dict(producto_id=f.p,cantidad=2)]),expected=200)
        self.assertEqual(quote['total'],20000)
        sale=await self.post('/ventas',dict(local_id=f.local,metodo_pago_id=f.method,politica='lista',importe_cobrado='200',detalles=[dict(producto_id=f.p,cantidad=2)]))
        result=await self.post(f'/ventas/{sale["id"]}/devoluciones',dict(motivo_id=f.reason,metodo_reintegro_id=f.method,detalle='Cambio solicitado',productos_aptos=True,detalles=[dict(producto_id=f.p,cantidad=1)]))
        self.assertEqual(result['devoluciones'][0]['total'],10000)
        self.assertEqual(result['detalles'][0]['costo_unitario'],6000)
        inventory=(await self.client.get('/api/inventario')).json()
        self.assertEqual(next(r['disponible'] for r in inventory if r['establecimiento_id']==f.local and r['producto_id']==f.p),4)
        reports=(await self.client.get('/api/reportes')).json()
        self.assertEqual(reports['ventas'][0]['neto'],10000)
        history=(await self.client.get('/api/reposiciones')).json()[0]['remitos'][0]['bultos'][0]['historial']
        self.assertEqual(len(history),5)

    async def test_validation_rejects_negative_fractional_or_empty_quantities(self):
        for quantity in (-1,0,1.5,True):
            result=await self.client.post('/api/reposiciones',json=dict(establecimiento_solicitante_id=self.f.local,establecimiento_proveedor_id=self.f.cd,detalles=[dict(producto_id=self.f.p,cantidad=quantity)]))
            self.assertEqual(result.status_code,422,result.text)
        result=await self.client.post('/api/reposiciones',json=dict(establecimiento_solicitante_id=self.f.local,establecimiento_proveedor_id=self.f.cd,detalles=[]))
        self.assertEqual(result.status_code,422)

    async def test_client_cannot_override_historical_cost_or_total(self):
        self.f.supply()
        for field in ('costo_unitario','total'):
            data=dict(local_id=self.f.local,metodo_pago_id=self.f.method,politica='lista',importe_cobrado='100',detalles=[dict(producto_id=self.f.p,cantidad=1)])
            data[field]=0
            result=await self.client.post('/api/ventas',json=data)
            self.assertEqual(result.status_code,422)
        self.assertEqual(self.f.sales.list(),[])

    async def test_read_endpoints_and_openapi(self):
        for path in ('/api/salud','/api/catalogos','/api/compras','/api/reposiciones','/api/ventas','/api/inventario','/api/inventario/movimientos','/api/reportes','/openapi.json'):
            result=await self.client.get(path)
            self.assertEqual(result.status_code,200,(path,result.text))
        schema=(await self.client.get('/openapi.json')).json()
        self.assertIn('ProductInput',schema['components']['schemas'])
        self.assertIn('/api/catalogos/producto',schema['paths'])

    async def test_not_found_conflict_and_date_errors(self):
        self.assertEqual((await self.client.get('/api/ventas/999')).status_code,404)
        self.assertEqual((await self.client.get('/api/reportes?desde=2026-12-01&hasta=2026-01-01')).status_code,409)
        self.assertEqual((await self.client.get('/api/reportes?desde=inválido')).status_code,422)
        await self.post('/catalogos/proveedor',dict(nombre='Repetido',CUIT='30000000000',esta_activo=True),expected=409)
        await self.post('/demo',expected=409)

    async def test_catalog_update_and_minimum(self):
        result=await self.client.put('/api/catalogos/producto/'+str(self.f.p),json=dict(nombre='Arroz nuevo',codigo='A',detalle='',categoria_id=self.f.category,precio='150.25',costo_referencia='65.25',esta_activo=True))
        self.assertEqual(result.status_code,200,result.text)
        self.assertEqual(result.json()['precio'],15025)
        result=await self.client.put('/api/inventario/minimo',json=dict(establecimiento_id=self.f.local,producto_id=self.f.p,minimo_permitido=7))
        self.assertEqual(result.status_code,200)
        row=next(r for r in (await self.client.get('/api/inventario')).json() if r['producto_id']==self.f.p and r['establecimiento_id']==self.f.local)
        self.assertEqual(row['faltante'],7)

    async def test_cors_allows_local_frontend(self):
        response=await self.client.options('/api/ventas',headers={'Origin':'http://127.0.0.1:5173','Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'Content-Type'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.headers['access-control-allow-origin'],'http://127.0.0.1:5173')
        response=await self.client.options('/api/ventas',headers={'Origin':'https://otro-sitio.example','Access-Control-Request-Method':'POST'})
        self.assertEqual(response.status_code,400)

    async def test_cross_site_write_is_rejected_even_without_body(self):
        response=await self.client.post('/api/demo',headers={'Origin':'https://otro-sitio.example'})
        self.assertEqual(response.status_code,403)
        self.assertEqual(len(self.f.catalog.list_all()['establecimiento']),3)
