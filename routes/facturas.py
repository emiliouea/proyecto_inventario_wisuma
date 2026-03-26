from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from services.cliente_service import ClienteService
from services.factura_service import FacturaService
from services.producto_service import ProductoService
from services.reporte_service import generar_reporte_facturas
from forms.factura_form import validar_factura_form

facturas_bp = Blueprint('facturas', __name__, url_prefix='/facturas')


@facturas_bp.route('/')
@login_required
def index():
    lista = FacturaService.obtener_todas()
    return render_template('facturas/index.html', facturas=[f.to_dict() for f in lista])


@facturas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    if request.method == 'POST':
        errores, datos = validar_factura_form(request.form)
        if errores:
            for e in errores:
                flash(e, 'error')
        else:
            try:
                FacturaService.crear(datos['cliente_id'], datos['items'])
                flash('Factura creada exitosamente.', 'success')
                return redirect(url_for('facturas.index'))
            except Exception as ex:
                flash(f'Error al crear factura: {ex}', 'error')

    return render_template('facturas/form.html',
                           clientes=ClienteService.obtener_todos(),
                           productos=ProductoService.obtener_todos())


@facturas_bp.route('/<int:factura_id>')
@login_required
def detalle(factura_id):
    factura = FacturaService.obtener_por_id(factura_id)
    if not factura:
        flash('Factura no encontrada.', 'error')
        return redirect(url_for('facturas.index'))
    return render_template('facturas/detalle.html', factura=factura.to_dict())


@facturas_bp.route('/<int:factura_id>/estado', methods=['POST'])
@login_required
def estado(factura_id):
    estado = request.form.get('estado', 'Pendiente')
    if FacturaService.cambiar_estado(factura_id, estado):
        flash(f'Estado actualizado a "{estado}".', 'success')
    else:
        flash('Factura no encontrada.', 'error')
    return redirect(url_for('facturas.detalle', factura_id=factura_id))


@facturas_bp.route('/<int:factura_id>/eliminar', methods=['POST'])
@login_required
def eliminar(factura_id):
    if FacturaService.eliminar(factura_id):
        flash('Factura eliminada.', 'success')
    else:
        flash('Factura no encontrada.', 'error')
    return redirect(url_for('facturas.index'))


@facturas_bp.route('/reporte/pdf')
@login_required
def reporte_pdf():
    buffer = generar_reporte_facturas(FacturaService.obtener_todas())
    return send_file(buffer, mimetype='application/pdf',
                     download_name='reporte_facturas.pdf', as_attachment=False)
