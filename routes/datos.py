from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from inventario.productos import Producto

datos_bp = Blueprint('datos', __name__, url_prefix='/datos')


def get_inventario():
    from app import inventario
    return inventario


@datos_bp.route('/txt')
@login_required
def txt():
    inv = get_inventario()
    data, mensaje = inv.cargar_productos_txt()
    if not data:
        flash(mensaje, 'info')
    return render_template('datos.html', data=data, tipo='TXT')


@datos_bp.route('/txt/guardar', methods=['POST'])
@login_required
def guardar_txt():
    exito, mensaje = get_inventario().guardar_productos_txt()
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('datos.txt'))


@datos_bp.route('/txt/cargar', methods=['POST'])
@login_required
def cargar_txt():
    inv = get_inventario()
    data, mensaje = inv.cargar_productos_txt()
    for d in data:
        inv.agregar_producto(Producto.from_dict(d))
    flash(mensaje, 'success')
    return redirect(url_for('datos.txt'))


@datos_bp.route('/json')
@login_required
def json_view():
    inv = get_inventario()
    data, mensaje = inv.cargar_productos_json()
    if not data:
        flash(mensaje, 'info')
    return render_template('datos.html', data=data, tipo='JSON')


@datos_bp.route('/json/guardar', methods=['POST'])
@login_required
def guardar_json():
    exito, mensaje = get_inventario().guardar_productos_json()
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('datos.json_view'))


@datos_bp.route('/json/cargar', methods=['POST'])
@login_required
def cargar_json():
    inv = get_inventario()
    data, mensaje = inv.cargar_productos_json()
    for d in data:
        inv.agregar_producto(Producto.from_dict(d))
    flash(mensaje, 'success')
    return redirect(url_for('datos.json_view'))


@datos_bp.route('/csv')
@login_required
def csv_view():
    inv = get_inventario()
    data, mensaje = inv.cargar_productos_csv()
    if not data:
        flash(mensaje, 'info')
    return render_template('datos.html', data=data, tipo='CSV')


@datos_bp.route('/csv/guardar', methods=['POST'])
@login_required
def guardar_csv():
    exito, mensaje = get_inventario().guardar_productos_csv()
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('datos.csv_view'))


@datos_bp.route('/csv/cargar', methods=['POST'])
@login_required
def cargar_csv():
    inv = get_inventario()
    data, mensaje = inv.cargar_productos_csv()
    for d in data:
        inv.agregar_producto(Producto.from_dict(d))
    flash(mensaje, 'success')
    return redirect(url_for('datos.csv_view'))
