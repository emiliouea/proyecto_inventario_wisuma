from inventario.database import db
from models.factura import Factura, FacturaDetalle
from inventario.productos import Producto


class FacturaService:

    @staticmethod
    def obtener_todas():
        return Factura.query.order_by(Factura.fecha.desc()).all()

    @staticmethod
    def obtener_por_id(factura_id):
        return Factura.query.get(factura_id)

    @staticmethod
    def crear(cliente_id, items):
        """
        items: lista de dicts con {producto_id, cantidad}
        Descuenta stock automáticamente.
        """
        factura = Factura(cliente_id=cliente_id)
        db.session.add(factura)
        db.session.flush()  # obtener factura.id antes del commit

        for item in items:
            producto = Producto.query.get(item['producto_id'])
            if not producto:
                continue
            cantidad = int(item['cantidad'])
            subtotal = round(producto.precio * cantidad, 2)
            detalle = FacturaDetalle(
                factura_id=factura.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal
            )
            db.session.add(detalle)
            producto.stock = max(0, producto.stock - cantidad)

        db.session.flush()
        factura.calcular_total()
        db.session.commit()
        return factura

    @staticmethod
    def cambiar_estado(factura_id, estado):
        factura = Factura.query.get(factura_id)
        if not factura:
            return None
        factura.estado = estado
        db.session.commit()
        return factura

    @staticmethod
    def eliminar(factura_id):
        factura = Factura.query.get(factura_id)
        if not factura:
            return False
        db.session.delete(factura)
        db.session.commit()
        return True
