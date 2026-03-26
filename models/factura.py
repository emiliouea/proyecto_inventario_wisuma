from datetime import datetime
from inventario.database import db


class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='Pendiente')  # Pendiente, Pagada, Anulada
    total = db.Column(db.Float, default=0.0)

    cliente = db.relationship('Cliente', backref=db.backref('facturas', lazy=True))
    detalles = db.relationship('FacturaDetalle', backref='factura', lazy=True, cascade='all, delete-orphan')

    def calcular_total(self):
        self.total = sum(d.subtotal for d in self.detalles)
        return self.total

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nombre': self.cliente.nombre if self.cliente else '',
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M') if self.fecha else '',
            'estado': self.estado,
            'total': self.total,
            'detalles': [d.to_dict() for d in self.detalles]
        }

    def __repr__(self):
        return f"<Factura #{self.id}>"


class FacturaDetalle(db.Model):
    __tablename__ = 'factura_detalles'

    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('facturas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto', backref=db.backref('detalles_factura', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'factura_id': self.factura_id,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto.nombre if self.producto else '',
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }

    def __repr__(self):
        return f"<FacturaDetalle factura={self.factura_id} producto={self.producto_id}>"
