from datetime import datetime
from .database import db # Import db from the new database module

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False, default='General') # Nueva columna
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nombre, categoria, descripcion, precio, stock, id=None):
        if id is not None:
            self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

    @staticmethod
    def from_dict(data):
        _id = data.get('id')
        return Producto(
            id=_id,
            nombre=data['nombre'],
            categoria=data.get('categoria', 'General'),
            descripcion=data.get('descripcion', ''),
            precio=float(data['precio']),
            stock=int(data['stock'])
        )

    def __repr__(self):
        return f"<Producto {self.nombre}>"
