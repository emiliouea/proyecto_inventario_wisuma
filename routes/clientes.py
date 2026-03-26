from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from inventario.clientes import Cliente

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')


def get_inventario():
    from app import inventario
    return inventario


@clientes_bp.route('/')
@login_required
def index():
    lista = get_inventario().obtener_todos_clientes()
    return render_template('clientes/index.html', clientes=[c.to_dict() for c in lista])


@clientes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            tipo=request.form['tipo']
        )
        exito, mensaje = get_inventario().agregar_cliente(cliente)
        flash(mensaje, 'success' if exito else 'error')
        if exito:
            return redirect(url_for('clientes.index'))

    return render_template('clientes/form.html', cliente=None, accion='Agregar')


@clientes_bp.route('/editar/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def editar(cliente_id):
    inv = get_inventario()
    cliente = inv.obtener_cliente_por_id(cliente_id)
    if not cliente:
        flash('Cliente no encontrado', 'error')
        return redirect(url_for('clientes.index'))

    if request.method == 'POST':
        exito, mensaje = inv.actualizar_cliente(
            cliente_id,
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            tipo=request.form['tipo']
        )
        flash(mensaje, 'success' if exito else 'error')
        if exito:
            return redirect(url_for('clientes.index'))

    return render_template('clientes/form.html', cliente=cliente.to_dict(), accion='Editar')


@clientes_bp.route('/eliminar/<int:cliente_id>', methods=['POST'])
@login_required
def eliminar(cliente_id):
    exito, mensaje = get_inventario().eliminar_cliente(cliente_id)
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('clientes.index'))
