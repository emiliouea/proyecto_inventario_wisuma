CATEGORIAS_FERRETERIA = [
    'Herramientas Manuales',
    'Herramientas Eléctricas',
    'Materiales de Construcción',
    'Plomería',
    'Electricidad',
    'Pintura',
    'Fijaciones y Tornillería',
    'Seguridad',
    'Jardinería',
    'General'
]


def validar_producto_form(form_data):
    """Valida los datos del formulario de producto. Retorna (errores, datos_limpios)."""
    errores = []
    datos = {}

    nombre = form_data.get('nombre', '').strip()
    if not nombre:
        errores.append('El nombre es obligatorio.')
    elif len(nombre) > 100:
        errores.append('El nombre no puede superar 100 caracteres.')
    else:
        datos['nombre'] = nombre

    categoria = form_data.get('categoria', '').strip()
    if not categoria:
        errores.append('La categoría es obligatoria.')
    else:
        datos['categoria'] = categoria

    try:
        precio = float(form_data.get('precio', 0))
        if precio < 0:
            errores.append('El precio no puede ser negativo.')
        else:
            datos['precio'] = precio
    except (ValueError, TypeError):
        errores.append('El precio debe ser un número válido.')

    try:
        stock = int(form_data.get('stock', 0))
        if stock < 0:
            errores.append('El stock no puede ser negativo.')
        else:
            datos['stock'] = stock
    except (ValueError, TypeError):
        errores.append('El stock debe ser un número entero.')

    datos['descripcion'] = form_data.get('descripcion', '').strip()

    return errores, datos
