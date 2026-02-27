"""
Módulo del modelo Cliente
Implementa la clase Cliente con encapsulamiento completo
"""

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
