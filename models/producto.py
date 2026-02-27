"""
Módulo del modelo Producto
Implementa la clase Producto con encapsulamiento completo
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
