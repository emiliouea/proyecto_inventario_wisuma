from .database import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    tipo = db.Column(db.String(50)) # Por ejemplo: 'Particular', 'Empresa'

    def __init__(self, nombre, telefono, email, tipo, id=None):
        if id is not None:
            self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.tipo = tipo

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'tipo': self.tipo
        }

    @staticmethod
    def from_dict(data):
        _id = data.get('id')
        return Cliente(
            id=_id,
            nombre=data['nombre'],
            telefono=data.get('telefono', None),
            email=data.get('email', None),
            tipo=data.get('tipo', None)
        )
    
    def __repr__(self):
        return f"<Cliente {self.nombre}>"
