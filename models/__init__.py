"""
Paquete de modelos del Sistema de Gestión de Inventario
Exporta las clases Producto, Cliente y Factura
"""

from .producto import Producto
from .cliente import Cliente
from .factura import Factura

__all__ = ['Producto', 'Cliente', 'Factura']
