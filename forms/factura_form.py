ESTADOS_FACTURA = ['Pendiente', 'Pagada', 'Anulada']


def validar_factura_form(form_data):
    """Valida los datos del formulario de factura. Retorna (errores, datos_limpios)."""
    errores = []
    datos = {}

    try:
        cliente_id = int(form_data.get('cliente_id', 0))
        if cliente_id <= 0:
            errores.append('Debe seleccionar un cliente.')
        else:
            datos['cliente_id'] = cliente_id
    except (ValueError, TypeError):
        errores.append('Cliente inválido.')

    # items: producto_id[] y cantidad[]
    productos_ids = form_data.getlist('producto_id[]')
    cantidades = form_data.getlist('cantidad[]')

    items = []
    for pid, cant in zip(productos_ids, cantidades):
        try:
            pid_int = int(pid)
            cant_int = int(cant)
            if pid_int > 0 and cant_int > 0:
                items.append({'producto_id': pid_int, 'cantidad': cant_int})
        except (ValueError, TypeError):
            continue

    if not items:
        errores.append('Debe agregar al menos un producto a la factura.')
    else:
        datos['items'] = items

    return errores, datos
