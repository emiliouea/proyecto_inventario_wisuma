"""
Módulo de gestión de inventario
Implementa la clase Inventario con operaciones CRUD usando colecciones de Python
"""

import sqlite3
from database import Database
from models import Producto, Cliente, Factura


class Inventario:
    """
    Clase para gestionar el inventario de productos
    Utiliza diccionarios, listas y conjuntos para operaciones eficientes
    """
    
    def __init__(self):
        self.db = Database()
        self.db.insertar_datos_ejemplo()
        # Diccionario para búsqueda rápida por código: {codigo: Producto}
        self._productos_cache = {}
        # Conjunto para códigos únicos
        self._codigos_unicos = set()
        # Lista de categorías disponibles
        self._categorias = []
    
    # ==================== OPERACIONES CRUD DE PRODUCTOS ====================
    
    def agregar_producto(self, producto):
        """
        Añade un nuevo producto al inventario
        Args:
            producto: Objeto de tipo Producto
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, categoria, precio, stock, ubicacion, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (producto.codigo, producto.nombre, producto.categoria, producto.precio,
                  producto.stock, producto.ubicacion, producto.descripcion))
            
            conn.commit()
            producto.id = cursor.lastrowid
            conn.close()
            
            # Actualizar cache
            self._productos_cache[producto.codigo] = producto
            self._codigos_unicos.add(producto.codigo)
            
            return True, f"Producto {producto.nombre} agregado exitosamente"
        except sqlite3.IntegrityError:
            return False, f"El código {producto.codigo} ya existe"
        except Exception as e:
            return False, f"Error al agregar producto: {str(e)}"
    
    def obtener_producto_por_id(self, producto_id):
        """
        Obtiene un producto por su ID
        Args:
            producto_id: ID del producto
        Returns:
            Producto o None
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Producto(
                id=row['id'],
                codigo=row['codigo'],
                nombre=row['nombre'],
                categoria=row['categoria'],
                precio=row['precio'],
                stock=row['stock'],
                ubicacion=row['ubicacion'],
                descripcion=row['descripcion']
            )
        return None
    
    def obtener_producto_por_codigo(self, codigo):
        """
        Obtiene un producto por su código
        Utiliza cache para búsqueda rápida
        """
        # Intentar obtener del cache
        if codigo in self._productos_cache:
            return self._productos_cache[codigo]
        
        # Si no está en cache, buscar en BD
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE codigo = ?', (codigo,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            producto = Producto(
                id=row['id'],
                codigo=row['codigo'],
                nombre=row['nombre'],
                categoria=row['categoria'],
                precio=row['precio'],
                stock=row['stock'],
                ubicacion=row['ubicacion'],
                descripcion=row['descripcion']
            )
            # Guardar en cache
            self._productos_cache[codigo] = producto
            return producto
        return None
    
    def actualizar_producto(self, producto_id, **kwargs):
        """
        Actualiza un producto existente
        Args:
            producto_id: ID del producto
            **kwargs: Campos a actualizar (nombre, precio, stock, etc.)
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            # Construir query dinámicamente
            campos = []
            valores = []
            for key, value in kwargs.items():
                if key in ['nombre', 'categoria', 'precio', 'stock', 'ubicacion', 'descripcion', 'codigo']:
                    campos.append(f"{key} = ?")
                    valores.append(value)
            
            if not campos:
                return False, "No hay campos para actualizar"
            
            valores.append(producto_id)
            query = f"UPDATE productos SET {', '.join(campos)} WHERE id = ?"
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            
            if cursor.rowcount > 0:
                conn.close()
                # Limpiar cache para forzar recarga
                self._productos_cache.clear()
                return True, "Producto actualizado exitosamente"
            else:
                conn.close()
                return False, "Producto no encontrado"
        except Exception as e:
            return False, f"Error al actualizar producto: {str(e)}"
    
    def eliminar_producto(self, producto_id):
        """
        Elimina un producto del inventario
        Args:
            producto_id: ID del producto
        Returns:
            tuple: (éxito: bool, mensaje: str)
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Obtener código antes de eliminar para limpiar cache
            cursor.execute('SELECT codigo FROM productos WHERE id = ?', (producto_id,))
            row = cursor.fetchone()
            
            if row:
                codigo = row['codigo']
                cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
                conn.commit()
                conn.close()
                
                # Limpiar cache
                if codigo in self._productos_cache:
                    del self._productos_cache[codigo]
                if codigo in self._codigos_unicos:
                    self._codigos_unicos.remove(codigo)
                
                return True, "Producto eliminado exitosamente"
            else:
                conn.close()
                return False, "Producto no encontrado"
        except Exception as e:
            return False, f"Error al eliminar producto: {str(e)}"
    
    def buscar_productos_por_nombre(self, nombre):
        """
        Busca productos por nombre (búsqueda parcial)
        Returns:
            Lista de objetos Producto
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE nombre LIKE ?', (f'%{nombre}%',))
        rows = cursor.fetchall()
        conn.close()
        
        productos = []
        for row in rows:
            productos.append(Producto(
                id=row['id'],
                codigo=row['codigo'],
                nombre=row['nombre'],
                categoria=row['categoria'],
                precio=row['precio'],
                stock=row['stock'],
                ubicacion=row['ubicacion'],
                descripcion=row['descripcion']
            ))
        return productos
    
    def obtener_todos_productos(self):
        """
        Obtiene todos los productos del inventario
        Returns:
            Lista de objetos Producto
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos ORDER BY nombre')
        rows = cursor.fetchall()
        conn.close()
        
        productos = []
        for row in rows:
            productos.append(Producto(
                id=row['id'],
                codigo=row['codigo'],
                nombre=row['nombre'],
                categoria=row['categoria'],
                precio=row['precio'],
                stock=row['stock'],
                ubicacion=row['ubicacion'],
                descripcion=row['descripcion']
            ))
        return productos
    
    def obtener_productos_por_categoria(self, categoria):
        """
        Obtiene productos filtrados por categoría
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE categoria = ? ORDER BY nombre', (categoria,))
        rows = cursor.fetchall()
        conn.close()
        
        productos = []
        for row in rows:
            productos.append(Producto(
                id=row['id'],
                codigo=row['codigo'],
                nombre=row['nombre'],
                categoria=row['categoria'],
                precio=row['precio'],
                stock=row['stock'],
                ubicacion=row['ubicacion'],
                descripcion=row['descripcion']
            ))
        return productos
    
    def obtener_categorias(self):
        """
        Obtiene lista única de categorías usando conjunto
        Returns:
            Lista de categorías únicas
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT categoria FROM productos ORDER BY categoria')
        rows = cursor.fetchall()
        conn.close()
        
        # Usar conjunto para garantizar unicidad
        categorias = set()
        for row in rows:
            if row['categoria']:
                categorias.add(row['categoria'])
        
        return sorted(list(categorias))
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas del inventario usando colecciones
        Returns:
            Diccionario con estadísticas
        """
        productos = self.obtener_todos_productos()
        
        if not productos:
            return {
                'total_productos': 0,
                'valor_total': 0,
                'stock_total': 0,
                'categorias': [],
                'productos_bajo_stock': []
            }
        
        # Usar diccionario para agrupar por categoría
        productos_por_categoria = {}
        valor_total = 0
        stock_total = 0
        productos_bajo_stock = []
        
        for producto in productos:
            # Agrupar por categoría
            if producto.categoria not in productos_por_categoria:
                productos_por_categoria[producto.categoria] = []
            productos_por_categoria[producto.categoria].append(producto)
            
            # Calcular totales
            valor_total += producto.precio * producto.stock
            stock_total += producto.stock
            
            # Detectar productos con bajo stock (menos de 20 unidades)
            if producto.stock < 20:
                productos_bajo_stock.append(producto)
        
        return {
            'total_productos': len(productos),
            'valor_total': valor_total,
            'stock_total': stock_total,
            'categorias': list(productos_por_categoria.keys()),
            'productos_por_categoria': productos_por_categoria,
            'productos_bajo_stock': productos_bajo_stock
        }
    
    # ==================== OPERACIONES CRUD DE CLIENTES ====================
    
    def agregar_cliente(self, cliente):
        """Añade un nuevo cliente"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO clientes (nombre, telefono, email, tipo)
                VALUES (?, ?, ?, ?)
            ''', (cliente.nombre, cliente.telefono, cliente.email, cliente.tipo))
            
            conn.commit()
            cliente.id = cursor.lastrowid
            conn.close()
            
            return True, f"Cliente {cliente.nombre} agregado exitosamente"
        except Exception as e:
            return False, f"Error al agregar cliente: {str(e)}"
    
    def obtener_todos_clientes(self):
        """Obtiene todos los clientes"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY nombre')
        rows = cursor.fetchall()
        conn.close()
        
        clientes = []
        for row in rows:
            clientes.append(Cliente(
                id=row['id'],
                nombre=row['nombre'],
                telefono=row['telefono'],
                email=row['email'],
                tipo=row['tipo']
            ))
        return clientes
    
    def obtener_cliente_por_id(self, cliente_id):
        """Obtiene un cliente por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Cliente(
                id=row['id'],
                nombre=row['nombre'],
                telefono=row['telefono'],
                email=row['email'],
                tipo=row['tipo']
            )
        return None
    
    def actualizar_cliente(self, cliente_id, **kwargs):
        """Actualiza un cliente"""
        try:
            campos = []
            valores = []
            for key, value in kwargs.items():
                if key in ['nombre', 'telefono', 'email', 'tipo']:
                    campos.append(f"{key} = ?")
                    valores.append(value)
            
            if not campos:
                return False, "No hay campos para actualizar"
            
            valores.append(cliente_id)
            query = f"UPDATE clientes SET {', '.join(campos)} WHERE id = ?"
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            
            if cursor.rowcount > 0:
                conn.close()
                return True, "Cliente actualizado exitosamente"
            else:
                conn.close()
                return False, "Cliente no encontrado"
        except Exception as e:
            return False, f"Error al actualizar cliente: {str(e)}"
    
    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                conn.close()
                return True, "Cliente eliminado exitosamente"
            else:
                conn.close()
                return False, "Cliente no encontrado"
        except Exception as e:
            return False, f"Error al eliminar cliente: {str(e)}"
    
    # ==================== OPERACIONES DE FACTURAS ====================
    
    def obtener_todas_facturas(self):
        """Obtiene todas las facturas con información del cliente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT f.*, c.nombre as cliente_nombre
            FROM facturas f
            LEFT JOIN clientes c ON f.cliente_id = c.id
            ORDER BY f.fecha DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        facturas = []
        for row in rows:
            factura = Factura(
                id=row['id'],
                numero=row['numero'],
                fecha=row['fecha'],
                cliente_id=row['cliente_id'],
                total=row['total'],
                estado=row['estado']
            )
            # Agregar nombre del cliente como atributo adicional
            factura.cliente_nombre = row['cliente_nombre']
            facturas.append(factura)
        return facturas
