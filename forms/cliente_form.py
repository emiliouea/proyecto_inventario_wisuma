TIPOS_CLIENTE = ['Particular', 'Empresa', 'Contratista', 'Mayorista']


def validar_cliente_form(form_data):
    """Valida los datos del formulario de cliente. Retorna (errores, datos_limpios)."""
    errores = []
    datos = {}

    nombre = form_data.get('nombre', '').strip()
    if not nombre:
        errores.append('El nombre es obligatorio.')
    elif len(nombre) > 100:
        errores.append('El nombre no puede superar 100 caracteres.')
    else:
        datos['nombre'] = nombre

    datos['telefono'] = form_data.get('telefono', '').strip()
    datos['email'] = form_data.get('email', '').strip()
    datos['tipo'] = form_data.get('tipo', 'Particular').strip()

    return errores, datos
