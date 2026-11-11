from sqlalchemy import select, func
from . import models as m

MODELS = {model.__tablename__: model for model in m.Base.__subclasses__()}


def record(instance):
    return {col.name: getattr(instance, col.name) for col in instance.__table__.columns}


class SqlAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def get(self, table, id):
        instance = self.session.get(MODELS[table], id)
        return record(instance) if instance else None

    def list(self, table, **filters):
        cls = MODELS[table]
        statement = select(cls).filter_by(**filters).order_by(cls.id)
        return [record(row) for row in self.session.scalars(statement)]

    def create(self, table, data):
        instance = MODELS[table](**data)
        self.session.add(instance)
        self.session.flush()
        return record(instance)

    def update(self, table, id, data):
        instance = self.session.get(MODELS[table], id)
        for key, value in data.items():
            setattr(instance, key, value)
        self.session.flush()
        return record(instance)

    def stock(self, establishment, product):
        rows = self.list('existencia', establecimiento_id=establishment, producto_id=product)
        return rows[0] if rows else self.create('existencia', dict(establecimiento_id=establishment, producto_id=product, almacenado_total=0, reservado=0, minimo_permitido=0))

    def returned(self, sale, product):
        return self.session.scalar(select(func.coalesce(func.sum(m.DetalleDevolucion.cantidad), 0))
            .join(m.Devolucion, m.Devolucion.id == m.DetalleDevolucion.devolucion_id)
            .where(m.Devolucion.venta_id == sale, m.DetalleDevolucion.producto_id == product))
