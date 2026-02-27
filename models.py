"""
Módulo de modelos para el Sistema de Gestión de Inventario
Implementa POO con clases para Producto, Cliente, Factura e Inventario
"""

class Producto:
    """
    Clase que representa un producto en el inventario
    Atributos: id, codigo, nombre, categoria, precio, stock, ubicacion, descripcion
    """
    
    def __init__(self, id=None, codigo='', nombre='', categoria='', precio=0.0, 
                 stock=0, ubicacion='', descripcion=''):
        self.__id = id
        self.__codigo = codigo
        self.__nombre = nombre
        self.__categoria = categoria
        self.__precio = precio
        self.__stock = stock
        self.__ubicacion = ubicacion
        self.__descripcion = descripcion
    
    # Getters
    @property
    def id(self):
        return self.__id
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def categoria(self):
        return self.__categoria
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def stock(self):
        return self.__stock
    
    @property
    def ubicacion(self):
        return self.__ubicacion
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    # Setters
    @id.setter
    def id(self, value):
        self.__id = value
    
    @codigo.setter
    def codigo(self, value):
        self.__codigo = value
    
    @nombre.setter
    def nombre(self, value):
        self.__nombre = value
    
    @categoria.setter
    def categoria(self, value):
        self.__categoria = value
    
    @precio.setter
    def precio(self, value):
        if value >= 0:
            self.__precio = value
        else:
            raise ValueError("El precio no puede ser negativo")
    
    @stock.setter
    def stock(self, value):
        if value >= 0:
            self.__stock = value
        else:
            raise ValueError("El stock no puede ser negativo")
    
    @ubicacion.setter
    def ubicacion(self, value):
        self.__ubicacion = value
    
    @descripcion.setter
    def descripcion(self, value):
        self.__descripcion = value
    
    def to_dict(self):
        """Convierte el objeto Producto a diccionario"""
        return {
            'id': self.__id,
            'codigo': self.__codigo,
            'nombre': self.__nombre,
            'categoria': self.__categoria,
            'precio': self.__precio,
            'stock': self.__stock,
            'ubicacion': self.__ubicacion,
            'descripcion': self.__descripcion
        }
    
    def __str__(self):
        return f"Producto({self.__codigo} - {self.__nombre}, Stock: {self.__stock})"


class Cliente:
    """
    Clase que representa un cliente
    Atributos: id, nombre, telefono, email, tipo
    """
    
    def __init__(self, id=None, nombre='', telefono='', email='', tipo='Regular'):
        self.__id = id
        self.__nombre = nombre
        self.__telefono = telefono
        self.__email = email
        self.__tipo = tipo
    
    # Getters y Setters
    @property
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def telefono(self):
        return self.__telefono
    
    @property
    def email(self):
        return self.__email
    
    @property
    def tipo(self):
        return self.__tipo
    
    @id.setter
    def id(self, value):
        self.__id = value
    
    @nombre.setter
    def nombre(self, value):
        self.__nombre = value
    
    @telefono.setter
    def telefono(self, value):
        self.__telefono = value
    
    @email.setter
    def email(self, value):
        self.__email = value
    
    @tipo.setter
    def tipo(self, value):
        self.__tipo = value
    
    def to_dict(self):
        """Convierte el objeto Cliente a diccionario"""
        return {
            'id': self.__id,
            'nombre': self.__nombre,
            'telefono': self.__telefono,
            'email': self.__email,
            'tipo': self.__tipo
        }
    
    def __str__(self):
        return f"Cliente({self.__nombre} - {self.__tipo})"


class Factura:
    """
    Clase que representa una factura
    Atributos: id, numero, fecha, cliente_id, total, estado
    """
    
    def __init__(self, id=None, numero='', fecha='', cliente_id=None, total=0.0, estado='pendiente'):
        self.__id = id
        self.__numero = numero
        self.__fecha = fecha
        self.__cliente_id = cliente_id
        self.__total = total
        self.__estado = estado
    
    # Getters y Setters
    @property
    def id(self):
        return self.__id
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def fecha(self):
        return self.__fecha
    
    @property
    def cliente_id(self):
        return self.__cliente_id
    
    @property
    def total(self):
        return self.__total
    
    @property
    def estado(self):
        return self.__estado
    
    @id.setter
    def id(self, value):
        self.__id = value
    
    @numero.setter
    def numero(self, value):
        self.__numero = value
    
    @fecha.setter
    def fecha(self, value):
        self.__fecha = value
    
    @cliente_id.setter
    def cliente_id(self, value):
        self.__cliente_id = value
    
    @total.setter
    def total(self, value):
        if value >= 0:
            self.__total = value
        else:
            raise ValueError("El total no puede ser negativo")
    
    @estado.setter
    def estado(self, value):
        self.__estado = value
    
    def to_dict(self):
        """Convierte el objeto Factura a diccionario"""
        return {
            'id': self.__id,
            'numero': self.__numero,
            'fecha': self.__fecha,
            'cliente_id': self.__cliente_id,
            'total': self.__total,
            'estado': self.__estado
        }
    
    def __str__(self):
        return f"Factura({self.__numero} - Total: ${self.__total})"
