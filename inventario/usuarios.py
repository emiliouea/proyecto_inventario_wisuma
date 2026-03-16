from .database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre, mail, password, id_usuario=None):
        if id_usuario is not None:
            self.id_usuario = id_usuario
        self.nombre = nombre
        self.mail = mail
        self.password = password

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "mail": self.mail
            # omitimos password por seguridad
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id_usuario=data.get('id_usuario'),
            nombre=data['nombre'],
            mail=data['mail'],
            password=data.get('password', '')
        )

    def __repr__(self):
        return f"<Usuario {self.nombre}>"
