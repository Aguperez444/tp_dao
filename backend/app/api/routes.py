from datetime import date
from typing import Annotated
from fastapi import APIRouter, Request, Query
from . import schemas as s

router = APIRouter(prefix='/api')


def catalog_routes(table, schema):
    def create(data, request: Request):
        return request.app.state.catalog.save(table,data.model_dump())
    create.__annotations__['data'] = schema
    create.__name__ = 'crear_' + table
    def update(id: int, data, request: Request):
        return request.app.state.catalog.save(table,data.model_dump(),id)
    update.__annotations__['data'] = schema
    update.__name__ = 'editar_' + table
    router.add_api_route('/catalogos/'+table,create,methods=['POST'],status_code=201,tags=['Catálogos'])
    router.add_api_route('/catalogos/'+table+'/{id}',update,methods=['PUT'],tags=['Catálogos'])


for table,schema in [('categoria',s.NamedInput),('provincia',s.NamedInput),('ciudad',s.CityInput),('domicilio',s.AddressInput),('establecimiento',s.EstablishmentInput),('proveedor',s.SupplierInput),('producto',s.ProductInput),('motivo',s.NamedInput)]:
    catalog_routes(table,schema)


@router.get('/salud',tags=['Sistema'])
def health():
    return {'estado':'ok','version':'2.0.0'}


@router.get('/catalogos',tags=['Catálogos'])
def catalogs(request: Request):
    return request.app.state.catalog.list_all()


@router.get('/compras',tags=['Compras'])
def purchases(request: Request):
    return request.app.state.purchasing.list()


@router.post('/compras',status_code=201,tags=['Compras'])
def purchase(data: s.PurchaseInput,request: Request):
    return request.app.state.purchasing.create(data.model_dump())


@router.post('/compras/{id}/recepcion',tags=['Compras'])
def receive_purchase(id: int,request: Request):
    return request.app.state.purchasing.receive(id)


@router.get('/reposiciones',tags=['Logística'])
def orders(request: Request):
    return request.app.state.logistics.list_orders()


@router.post('/reposiciones',status_code=201,tags=['Logística'])
def order(data: s.OrderInput,request: Request):
    return request.app.state.logistics.create_order(data.model_dump())


@router.post('/reposiciones/{id}/remitos',status_code=201,tags=['Logística'])
def delivery(id: int,data: s.DeliveryInput,request: Request):
    return request.app.state.logistics.create_delivery(id,data.numero_remito)


@router.post('/remitos/{id}/bultos',status_code=201,tags=['Logística'])
def package(id: int,data: s.PackageInput,request: Request):
    return request.app.state.logistics.prepare(id,data.model_dump())


@router.post('/bultos/{id}/{accion}',tags=['Logística'])
def transition(id: int,accion: str,data: s.TransitionInput,request: Request):
    return request.app.state.logistics.transition(id,accion,data.model_dump())


@router.get('/ventas',tags=['Ventas'])
def sales(request: Request):
    return request.app.state.sales.list()


@router.post('/ventas/cotizacion',tags=['Ventas'])
def quote(data: s.QuoteInput,request: Request):
    return request.app.state.sales.quote(data.model_dump())


@router.post('/ventas',status_code=201,tags=['Ventas'])
def sale(data: s.SaleInput,request: Request):
    return request.app.state.sales.create(data.model_dump())


@router.get('/ventas/{id}',tags=['Ventas'])
def sale_detail(id: int,request: Request):
    return request.app.state.sales.get(id)


@router.post('/ventas/{id}/devoluciones',status_code=201,tags=['Ventas'])
def refund(id: int,data: s.RefundInput,request: Request):
    return request.app.state.sales.refund(id,data.model_dump())


@router.get('/inventario',tags=['Inventario'])
def inventory(request: Request,establecimiento_id: Annotated[int|None,Query(gt=0)]=None):
    return request.app.state.reporting.stock(establecimiento_id)


@router.put('/inventario/minimo',tags=['Inventario'])
def minimum(data: s.MinimumInput,request: Request):
    return request.app.state.catalog.minimum(data.establecimiento_id,data.producto_id,data.minimo_permitido)


@router.get('/inventario/movimientos',tags=['Inventario'])
def movements(request: Request,desde: date=date(2000,1,1),hasta: date|None=None,establecimiento_id: Annotated[int|None,Query(gt=0)]=None):
    return request.app.state.reporting.movements(desde,hasta or date.today(),establecimiento_id)


@router.get('/reportes',tags=['Reportes'])
def reports(request: Request,desde: date=date(2000,1,1),hasta: date|None=None,establecimiento_id: Annotated[int|None,Query(gt=0)]=None):
    return request.app.state.reporting.generate(desde,hasta or date.today(),establecimiento_id)


@router.post('/demo',status_code=201,tags=['Sistema'])
def demo(request: Request):
    from app.seed import seed
    seed(request.app.state.database)
    return {'mensaje':'Datos de demostración cargados.'}
