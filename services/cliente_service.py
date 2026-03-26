from inventario.database import db
from inventario.clientes import Cliente


class ClienteService:

    @staticmethod
    def obtener_todos():
        return Cliente.query.all()

    @staticmethod
    def obtener_por_id(cliente_id):
        return Cliente.query.get(cliente_id)

    @staticmethod
    def crear(nombre, telefono, email, tipo):
        cliente = Cliente(nombre=nombre, telefono=telefono, email=email, tipo=tipo)
        db.session.add(cliente)
        db.session.commit()
        return cliente

    @staticmethod
    def actualizar(cliente_id, **kwargs):
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return None
        for k, v in kwargs.items():
            setattr(cliente, k, v)
        db.session.commit()
        return cliente

    @staticmethod
    def eliminar(cliente_id):
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return False
        db.session.delete(cliente)
        db.session.commit()
        return True
