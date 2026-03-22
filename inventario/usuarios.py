from flask_login import UserMixin
from .database import db

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre, email, password, id_usuario=None):
        if id_usuario is not None:
            self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id_usuario)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "email": self.email
            # omitimos password por seguridad
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id_usuario=data.get('id_usuario'),
            nombre=data['nombre'],
            email=data.get('email', data.get('mail')),
            password=data.get('password', '')
        )

    def __repr__(self):
        return f"<Usuario {self.nombre}>"
