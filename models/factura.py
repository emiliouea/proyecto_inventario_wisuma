"""
Módulo del modelo Factura
Implementa la clase Factura con encapsulamiento completo
"""

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
