"""
Módulo de gestión de base de datos SQLite
Implementa la clase Database para manejar la conexión y operaciones CRUD
"""

import sqlite3


class Database:
    """
    Clase para gestionar la conexión y operaciones con SQLite
    """
    
    def __init__(self, db_name='inventario.db'):
        self.db_name = db_name
        self.crear_tablas()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
        return conn
    
    def crear_tablas(self):
        """Crea las tablas necesarias si no existen"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL,
                ubicacion TEXT,
                descripcion TEXT
            )
        ''')
        
        # Tabla de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT,
                tipo TEXT DEFAULT 'Regular'
            )
        ''')
        
        # Tabla de facturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                fecha TEXT NOT NULL,
                cliente_id INTEGER,
                total REAL NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insertar_datos_ejemplo(self):
        """Inserta datos de ejemplo si las tablas están vacías"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute('SELECT COUNT(*) FROM productos')
        if cursor.fetchone()[0] == 0:
            productos_ejemplo = [
                ('FER001', 'Martillo de Carpintero', 'Herramientas', 15.99, 45, 'Bodega A - Estante 3', 
                 'Martillo profesional con mango de madera, ideal para trabajos de carpintería.'),
                ('FER002', 'Destornillador Phillips', 'Herramientas', 8.50, 120, 'Bodega A - Estante 5',
                 'Destornillador de precisión con punta magnética.'),
                ('FER003', 'Taladro Eléctrico', 'Herramientas Eléctricas', 89.99, 12, 'Bodega B - Estante 1',
                 'Taladro eléctrico de 500W con velocidad variable y reversible.'),
                ('FER004', 'Pintura Látex Blanca', 'Pinturas', 25.00, 30, 'Bodega C - Estante 2',
                 'Pintura látex de alta calidad, rendimiento 12 m²/litro.'),
                ('FER005', 'Cemento Portland', 'Construcción', 12.50, 200, 'Bodega D - Piso',
                 'Cemento Portland tipo I, saco de 50kg.'),
                ('FER006', 'Cinta Métrica 5m', 'Herramientas', 6.75, 80, 'Bodega A - Estante 4',
                 'Cinta métrica retráctil de 5 metros con freno automático.')
            ]
            
            cursor.executemany('''
                INSERT INTO productos (codigo, nombre, categoria, precio, stock, ubicacion, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', productos_ejemplo)
        
        # Insertar clientes de ejemplo
        cursor.execute('SELECT COUNT(*) FROM clientes')
        if cursor.fetchone()[0] == 0:
            clientes_ejemplo = [
                ('Juan Pérez', '555-1234', 'juan@email.com', 'Regular'),
                ('María González', '555-5678', 'maria@email.com', 'Premium'),
                ('Carlos Rodríguez', '555-9012', 'carlos@email.com', 'Regular'),
                ('Ana Martínez', '555-3456', 'ana@email.com', 'Premium')
            ]
            
            cursor.executemany('''
                INSERT INTO clientes (nombre, telefono, email, tipo)
                VALUES (?, ?, ?, ?)
            ''', clientes_ejemplo)
        
        # Insertar facturas de ejemplo
        cursor.execute('SELECT COUNT(*) FROM facturas')
        if cursor.fetchone()[0] == 0:
            facturas_ejemplo = [
                ('FAC-001', '2026-02-15', 1, 125.50, 'pagado'),
                ('FAC-002', '2026-02-18', 2, 89.99, 'pagado'),
                ('FAC-003', '2026-02-20', 3, 250.00, 'pendiente'),
                ('FAC-004', '2026-02-21', 4, 45.75, 'pagado')
            ]
            
            cursor.executemany('''
                INSERT INTO facturas (numero, fecha, cliente_id, total, estado)
                VALUES (?, ?, ?, ?, ?)
            ''', facturas_ejemplo)
        
        conn.commit()
        conn.close()
