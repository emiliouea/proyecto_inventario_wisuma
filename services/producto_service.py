from inventario.database import db
from inventario.productos import Producto


class ProductoService:

    @staticmethod
    def obtener_todos():
        return Producto.query.all()

    @staticmethod
    def obtener_por_id(producto_id):
        return Producto.query.get(producto_id)

    @staticmethod
    def buscar_por_nombre(nombre):
        return Producto.query.filter(Producto.nombre.ilike(f'%{nombre}%')).all()

    @staticmethod
    def obtener_por_categoria(categoria):
        return Producto.query.filter_by(categoria=categoria).all()

    @staticmethod
    def obtener_categorias():
        rows = db.session.query(Producto.categoria).distinct().all()
        return [r[0] for r in rows]

    @staticmethod
    def crear(nombre, categoria, descripcion, precio, stock):
        producto = Producto(nombre=nombre, categoria=categoria,
                            descripcion=descripcion, precio=precio, stock=stock)
        db.session.add(producto)
        db.session.commit()
        return producto

    @staticmethod
    def actualizar(producto_id, **kwargs):
        producto = Producto.query.get(producto_id)
        if not producto:
            return None
        for k, v in kwargs.items():
            setattr(producto, k, v)
        db.session.commit()
        return producto

    @staticmethod
    def eliminar(producto_id):
        producto = Producto.query.get(producto_id)
        if not producto:
            return False
        db.session.delete(producto)
        db.session.commit()
        return True
