"""Mapeo relacional del der_5_tp_dao.jpg. Los importes se guardan en centavos."""
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Named:
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)


class Categoria(Named, Base):
    __tablename__ = 'categoria'


class Provincia(Named, Base):
    __tablename__ = 'provincia'


class Ciudad(Base):
    __tablename__ = 'ciudad'
    __table_args__ = (UniqueConstraint('nombre', 'provincia_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    provincia_id: Mapped[int] = mapped_column(ForeignKey('provincia.id'))


class Domicilio(Base):
    __tablename__ = 'domicilio'
    id: Mapped[int] = mapped_column(primary_key=True)
    calle: Mapped[str] = mapped_column(String(150))
    altura: Mapped[str] = mapped_column(String(30))
    ciudad_id: Mapped[int] = mapped_column(ForeignKey('ciudad.id'))


class Establecimiento(Base):
    __tablename__ = 'establecimiento'
    __table_args__ = (Index('unico_centro', 'es_central', unique=True, sqlite_where=text('es_central = 1')),)
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True)
    es_central: Mapped[bool] = mapped_column(Boolean, default=False)
    domicilio_id: Mapped[int] = mapped_column(ForeignKey('domicilio.id'))


class Proveedor(Base):
    __tablename__ = 'proveedor'
    id: Mapped[int] = mapped_column(primary_key=True)
    CUIT: Mapped[str] = mapped_column(String(11), unique=True)
    nombre: Mapped[str] = mapped_column(String(150))
    esta_activo: Mapped[bool] = mapped_column(Boolean, default=True)


class Producto(Base):
    __tablename__ = 'producto'
    __table_args__ = (CheckConstraint('precio > 0 AND costo_referencia >= 0'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150))
    detalle: Mapped[str] = mapped_column(Text, default='')
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categoria.id'))
    precio: Mapped[int] = mapped_column(Integer)
    costo_referencia: Mapped[int] = mapped_column(Integer)
    esta_activo: Mapped[bool] = mapped_column(Boolean, default=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True)


class Existencia(Base):
    __tablename__ = 'existencia'
    __table_args__ = (UniqueConstraint('establecimiento_id', 'producto_id'),
                      CheckConstraint('almacenado_total >= reservado AND reservado >= 0 AND minimo_permitido >= 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    establecimiento_id: Mapped[int] = mapped_column(ForeignKey('establecimiento.id'))
    producto_id: Mapped[int] = mapped_column(ForeignKey('producto.id'))
    almacenado_total: Mapped[int] = mapped_column(Integer, default=0)
    reservado: Mapped[int] = mapped_column(Integer, default=0)
    minimo_permitido: Mapped[int] = mapped_column(Integer, default=0)


class EstadoCompra(Named, Base):
    __tablename__ = 'estado_compra'


class Compra(Base):
    __tablename__ = 'compra'
    id: Mapped[int] = mapped_column(primary_key=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey('proveedor.id'))
    estado_id: Mapped[int] = mapped_column(ForeignKey('estado_compra.id'))
    fecha: Mapped[str] = mapped_column(String(40))


class DetalleCompra(Base):
    __tablename__ = 'detalle_compra'
    __table_args__ = (UniqueConstraint('compra_id', 'producto_id'), CheckConstraint('cantidad > 0 AND costo >= 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey('producto.id'))
    compra_id: Mapped[int] = mapped_column(ForeignKey('compra.id'))
    cantidad: Mapped[int] = mapped_column(Integer)
    costo: Mapped[int] = mapped_column(Integer)


class EstadoReposicion(Named, Base):
    __tablename__ = 'estado_reposicion'


class OrdenReposicion(Base):
    __tablename__ = 'orden_reposicion'
    __table_args__ = (CheckConstraint('establecimiento_solicitante_id <> establecimiento_proveedor_id'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    establecimiento_solicitante_id: Mapped[int] = mapped_column(ForeignKey('establecimiento.id'))
    establecimiento_proveedor_id: Mapped[int] = mapped_column(ForeignKey('establecimiento.id'))
    fecha: Mapped[str] = mapped_column(String(40))
    estado_id: Mapped[int] = mapped_column(ForeignKey('estado_reposicion.id'))


class DetalleReposicion(Base):
    __tablename__ = 'detalle_reposicion'
    __table_args__ = (UniqueConstraint('orden_id', 'producto_id'), CheckConstraint('cantidad > 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey('producto.id'))
    orden_id: Mapped[int] = mapped_column(ForeignKey('orden_reposicion.id'))
    cantidad: Mapped[int] = mapped_column(Integer)


class EstadoRemito(Named, Base):
    __tablename__ = 'estado_remito'


class Remito(Base):
    __tablename__ = 'remito'
    id: Mapped[int] = mapped_column(primary_key=True)
    orden_reposicion_id: Mapped[int] = mapped_column(ForeignKey('orden_reposicion.id'))
    estado_remito_id: Mapped[int] = mapped_column(ForeignKey('estado_remito.id'))
    numero_remito: Mapped[str] = mapped_column(String(50), unique=True)
    fecha_emision: Mapped[str] = mapped_column(String(40))


class EstadoPrecinto(Named, Base):
    __tablename__ = 'estado_precinto'


class EstadoBulto(Named, Base):
    __tablename__ = 'estado_bulto'


class Bulto(Base):
    __tablename__ = 'bulto'
    id: Mapped[int] = mapped_column(primary_key=True)
    remito_id: Mapped[int] = mapped_column(ForeignKey('remito.id'))
    estado_precinto_id: Mapped[int] = mapped_column(ForeignKey('estado_precinto.id'))
    estado_bulto_id: Mapped[int] = mapped_column(ForeignKey('estado_bulto.id'))
    codigo_precinto: Mapped[str | None] = mapped_column(String(60), unique=True)


class DetalleBulto(Base):
    __tablename__ = 'detalle_bulto'
    __table_args__ = (UniqueConstraint('bulto_id', 'producto_id'), CheckConstraint('cantidad > 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey('producto.id'))
    bulto_id: Mapped[int] = mapped_column(ForeignKey('bulto.id'))
    cantidad: Mapped[int] = mapped_column(Integer)


class CambioEstadoBulto(Base):
    __tablename__ = 'cambio_estado_bulto'
    id: Mapped[int] = mapped_column(primary_key=True)
    bulto_id: Mapped[int] = mapped_column(ForeignKey('bulto.id'), index=True)
    estado_bulto_id: Mapped[int] = mapped_column(ForeignKey('estado_bulto.id'))
    fecha: Mapped[str] = mapped_column(String(40))
    responsable: Mapped[str] = mapped_column(String(150))
    observacion: Mapped[str] = mapped_column(String(500))


class MetodoPago(Named, Base):
    __tablename__ = 'metodo_pago'


class Venta(Base):
    __tablename__ = 'venta'
    __table_args__ = (CheckConstraint('total > 0'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    local_id: Mapped[int] = mapped_column(ForeignKey('establecimiento.id'))
    metodo_pago_id: Mapped[int] = mapped_column(ForeignKey('metodo_pago.id'))
    total: Mapped[int] = mapped_column(Integer)
    fecha: Mapped[str] = mapped_column(String(40), index=True)
    numero_comprobante: Mapped[str] = mapped_column(String(50), unique=True)


class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    __table_args__ = (UniqueConstraint('venta_id', 'producto_id'),
                      CheckConstraint('cantidad > 0 AND precio_unitario > 0 AND descuento_aplicado >= 0 AND descuento_aplicado < precio_unitario AND costo_unitario >= 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey('producto.id'))
    venta_id: Mapped[int] = mapped_column(ForeignKey('venta.id'))
    cantidad: Mapped[int] = mapped_column(Integer)
    precio_unitario: Mapped[int] = mapped_column(Integer)
    descuento_aplicado: Mapped[int] = mapped_column(Integer)
    costo_unitario: Mapped[int] = mapped_column(Integer)


class Motivo(Named, Base):
    __tablename__ = 'motivo'


class Devolucion(Base):
    __tablename__ = 'devolucion'
    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey('venta.id'))
    motivo_id: Mapped[int] = mapped_column(ForeignKey('motivo.id'))
    metodo_reintegro_id: Mapped[int] = mapped_column(ForeignKey('metodo_pago.id'))
    detalle: Mapped[str] = mapped_column(String(500))
    fecha: Mapped[str] = mapped_column(String(40), index=True)


class DetalleDevolucion(Base):
    __tablename__ = 'detalle_devolucion'
    __table_args__ = (UniqueConstraint('devolucion_id', 'producto_id'), CheckConstraint('cantidad > 0 AND importe_unitario >= 0'))
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey('producto.id'))
    devolucion_id: Mapped[int] = mapped_column(ForeignKey('devolucion.id'))
    cantidad: Mapped[int] = mapped_column(Integer)
    importe_unitario: Mapped[int] = mapped_column(Integer)
