"""
Módulo de gestión de inventario
Implementa la clase Inventario con operaciones CRUD usando colecciones de Python
"""


from .file_persistence import save_data_to_txt, load_data_from_txt, save_data_to_json, load_data_from_json, save_data_to_csv, load_data_from_csv

class Inventario:
    def __init__(self, app, db, Producto, Cliente):
        self.app = app
        self.db = db
        self.Producto = Producto
        self.Cliente = Cliente

    
    # ==================== OPERACIONES CRUD DE PRODUCTOS ====================
    
    def agregar_producto(self, producto):
        with self.app.app_context():
            nombre_producto = producto.nombre
            self.db.session.add(producto)
            self.db.session.commit()
        return True, f"Producto {nombre_producto} agregado exitosamente"

    def obtener_todos_productos(self):
        with self.app.app_context():
            return self.Producto.query.all()

    def obtener_producto_por_id(self, producto_id):
        with self.app.app_context():
            return self.Producto.query.get(producto_id)

    def actualizar_producto(self, producto_id, **kwargs):
        with self.app.app_context():
            producto = self.Producto.query.get(producto_id)
            if not producto:
                return False, "Producto no encontrado"
            for key, value in kwargs.items():
                setattr(producto, key, value)
            self.db.session.commit()
            return True, "Producto actualizado exitosamente"

    def eliminar_producto(self, producto_id):
        with self.app.app_context():
            producto = self.Producto.query.get(producto_id)
            if not producto:
                return False, "Producto no encontrado"
            self.db.session.delete(producto)
            self.db.session.commit()
            return True, "Producto eliminado exitosamente"

    def buscar_productos_por_nombre(self, nombre):
        with self.app.app_context():
            return self.Producto.query.filter(self.Producto.nombre.like(f'%{nombre}%')).all()

    def obtener_productos_por_categoria(self, categoria):
        with self.app.app_context():
            return self.Producto.query.filter_by(categoria=categoria).all()

    def obtener_categorias(self):
        with self.app.app_context():
            categorias = self.db.session.query(self.Producto.categoria).distinct().all()
            return [c[0] for c in categorias]

    # ==================== OPERACIONES CRUD DE CLIENTES ====================

    def agregar_cliente(self, cliente):
        with self.app.app_context():
            nombre_cliente = cliente.nombre
            self.db.session.add(cliente)
            self.db.session.commit()
        return True, f"Cliente {nombre_cliente} agregado exitosamente"

    def obtener_todos_clientes(self):
        with self.app.app_context():
            return self.Cliente.query.all()

    def obtener_cliente_por_id(self, cliente_id):
        with self.app.app_context():
            return self.Cliente.query.get(cliente_id)

    def actualizar_cliente(self, cliente_id, **kwargs):
        with self.app.app_context():
            cliente = self.Cliente.query.get(cliente_id)
            if not cliente:
                return False, "Cliente no encontrado"
            for key, value in kwargs.items():
                setattr(cliente, key, value)
            self.db.session.commit()
            return True, "Cliente actualizado exitosamente"

    def eliminar_cliente(self, cliente_id):
        with self.app.app_context():
            cliente = self.Cliente.query.get(cliente_id)
            if not cliente:
                return False, "Cliente no encontrado"
            self.db.session.delete(cliente)
            self.db.session.commit()
            return True, "Cliente eliminado exitosamente"

    def guardar_productos_txt(self, filename="datos.txt"):
        productos_dicts = [p.to_dict() for p in self.obtener_todos_productos()]
        return save_data_to_txt(productos_dicts, filename, delimiter='|')

    def cargar_productos_txt(self, filename="datos.txt"):
        keys = ["id", "codigo", "nombre", "categoria", "precio", "stock", "ubicacion", "descripcion"]
        data, mensaje = load_data_from_txt(filename, delimiter='|', keys=keys)
        productos = []
        for item_dict in data:
            try:
                # Convertir tipos de datos si es necesario
                item_dict['id'] = int(item_dict['id'])
                item_dict['precio'] = float(item_dict['precio'])
                item_dict['stock'] = int(item_dict['stock'])
                productos.append(Producto.from_dict(item_dict))
            except ValueError as e:
                print(f"Error al convertir datos de TXT: {e} en {item_dict}")
                continue
        return productos, mensaje

    def guardar_productos_csv(self, filename="datos.csv"):
        productos_dicts = [p.to_dict() for p in self.obtener_todos_productos()]
        if not productos_dicts:
            return False, "No hay productos para guardar en CSV."
        fieldnames = list(productos_dicts[0].keys())
        return save_data_to_csv(productos_dicts, filename, fieldnames)

    def cargar_productos_csv(self, filename="datos.csv"):
        data, mensaje = load_data_from_csv(filename)
        productos = []
        for item_dict in data:
            try:
                # Convertir tipos de datos si es necesario
                item_dict['id'] = int(item_dict['id']) if 'id' in item_dict and item_dict['id'] else None
                item_dict['precio'] = float(item_dict['precio']) if 'precio' in item_dict and item_dict['precio'] else 0.0
                item_dict['stock'] = int(item_dict['stock']) if 'stock' in item_dict and item_dict['stock'] else 0
                productos.append(Producto.from_dict(item_dict))
            except ValueError as e:
                print(f"Error al convertir datos de CSV: {e} en {item_dict}")
                continue
        return productos, mensaje

    def guardar_productos_json(self, filename="datos.json"):
        productos_dicts = [p.to_dict() for p in self.obtener_todos_productos()]
        return save_data_to_json(productos_dicts, filename)

    def cargar_productos_json(self, filename="datos.json"):
        data, mensaje = load_data_from_json(filename)
        productos = []
        for item_dict in data:
            try:
                productos.append(Producto.from_dict(item_dict))
            except Exception as e:
                print(f"Error al convertir datos de JSON: {e} en {item_dict}")
                continue
        return productos, mensaje
