from decimal import Decimal
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

Id = Annotated[int, Field(gt=0, strict=True)]
Quantity = Annotated[int, Field(gt=0, le=1_000_000, strict=True)]
Money = Annotated[Decimal, Field(ge=0, le=Decimal('999999999.99'), decimal_places=2)]
Name = Annotated[str, Field(min_length=1, max_length=150)]


class Input(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)


class NamedInput(Input):
    nombre: Name


class CityInput(NamedInput):
    provincia_id: Id


class AddressInput(Input):
    calle: Name
    altura: Annotated[str, Field(min_length=1,max_length=30)]
    ciudad_id: Id


class EstablishmentInput(NamedInput):
    es_central: bool = False
    domicilio_id: Id


class SupplierInput(NamedInput):
    CUIT: Annotated[str, Field(min_length=11,max_length=20)]
    esta_activo: bool = True


class ProductInput(NamedInput):
    codigo: Annotated[str, Field(min_length=1,max_length=50)]
    detalle: Annotated[str, Field(max_length=1000)] = ''
    categoria_id: Id
    precio: Money
    costo_referencia: Money
    esta_activo: bool = True


class LineInput(Input):
    producto_id: Id
    cantidad: Quantity


class PurchaseLineInput(LineInput):
    costo: Money


class PurchaseInput(Input):
    proveedor_id: Id
    detalles: Annotated[list[PurchaseLineInput], Field(min_length=1,max_length=100)]


class OrderInput(Input):
    establecimiento_solicitante_id: Id
    establecimiento_proveedor_id: Id
    detalles: Annotated[list[LineInput], Field(min_length=1,max_length=100)]


class DeliveryInput(Input):
    numero_remito: Annotated[str, Field(min_length=1,max_length=50)]


class PackageInput(Input):
    responsable: Name
    detalles: Annotated[list[LineInput], Field(min_length=1,max_length=100)]


class TransitionInput(Input):
    responsable: Name
    observacion: Annotated[str, Field(max_length=500)] = ''
    codigo_precinto: Annotated[str, Field(max_length=60)] = ''
    numero_remito: Annotated[str, Field(max_length=50)] = ''
    precinto_intacto: bool = False
    contenido_conforme: bool = False


class QuoteInput(Input):
    local_id: Id
    politica: Literal['lista','descuento_10'] = 'lista'
    detalles: Annotated[list[LineInput], Field(min_length=1,max_length=100)]


class SaleInput(QuoteInput):
    metodo_pago_id: Id
    importe_cobrado: Money


class RefundInput(Input):
    motivo_id: Id
    metodo_reintegro_id: Id
    detalle: Annotated[str, Field(min_length=1,max_length=500)]
    productos_aptos: bool
    detalles: Annotated[list[LineInput], Field(min_length=1,max_length=100)]


class MinimumInput(Input):
    establecimiento_id: Id
    producto_id: Id
    minimo_permitido: Annotated[int, Field(ge=0,le=1_000_000,strict=True)]
