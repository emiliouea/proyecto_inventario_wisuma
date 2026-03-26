from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from inventario.productos import Producto
from services.producto_service import ProductoService
from services.reporte_service import generar_reporte_productos

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')


def get_inventario():
    from app import inventario
    return inventario


@productos_bp.route('/')
@login_required
def index():
    inv = get_inventario()
    categoria = request.args.get('categoria', '')
    busqueda = request.args.get('busqueda', '')

    if categoria:
        lista = inv.obtener_productos_por_categoria(categoria)
    elif busqueda:
        lista = inv.buscar_productos_por_nombre(busqueda)
    else:
        lista = inv.obtener_todos_productos()

    return render_template('productos/index.html',
                           productos=[p.to_dict() for p in lista],
                           categorias=inv.obtener_categorias(),
                           categoria_actual=categoria,
                           busqueda_actual=busqueda)


@productos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    inv = get_inventario()
    if request.method == 'POST':
        producto = Producto(
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock']),
            descripcion=request.form['descripcion']
        )
        exito, mensaje = inv.agregar_producto(producto)
        flash(mensaje, 'success' if exito else 'error')
        if exito:
            return redirect(url_for('productos.index'))

    return render_template('productos/form.html',
                           producto=None,
                           categorias=inv.obtener_categorias(),
                           accion='Agregar')


@productos_bp.route('/editar/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar(producto_id):
    inv = get_inventario()
    producto = inv.obtener_producto_por_id(producto_id)
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos.index'))

    if request.method == 'POST':
        exito, mensaje = inv.actualizar_producto(
            producto_id,
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock']),
            descripcion=request.form['descripcion']
        )
        flash(mensaje, 'success' if exito else 'error')
        if exito:
            return redirect(url_for('productos.index'))

    return render_template('productos/form.html',
                           producto=producto.to_dict(),
                           categorias=inv.obtener_categorias(),
                           accion='Editar')


@productos_bp.route('/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar(producto_id):
    exito, mensaje = get_inventario().eliminar_producto(producto_id)
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('productos.index'))


@productos_bp.route('/detalle/<int:producto_id>')
@login_required
def detalle(producto_id):
    producto = get_inventario().obtener_producto_por_id(producto_id)
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos.index'))
    return render_template('productos/detalle.html',
                           producto_id=producto_id,
                           producto=producto.to_dict())


@productos_bp.route('/reporte/pdf')
@login_required
def reporte_pdf():
    buffer = generar_reporte_productos(ProductoService.obtener_todos())
    return send_file(buffer, mimetype='application/pdf',
                     download_name='reporte_productos.pdf', as_attachment=False)
