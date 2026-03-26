from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from inventario.usuarios import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


def get_inventario():
    from app import inventario
    return inventario


@usuarios_bp.route('/')
@login_required
def index():
    lista = get_inventario().obtener_todos_usuarios()
    return render_template('usuarios/index.html', usuarios=[u.to_dict() for u in lista])


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        usuario = Usuario(
            nombre=request.form['nombre'],
            email=request.form['email'],
            password=hashed
        )
        exito, mensaje = get_inventario().agregar_usuario(usuario)
        flash(mensaje, 'success' if exito else 'error')
        if exito:
            return redirect(url_for('usuarios.index'))

    return render_template('usuarios/form.html', usuario=None, accion='Agregar')


@usuarios_bp.route('/editar/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def editar(id_usuario):
    inv = get_inventario()
    usuario = inv.obtener_usuario_por_id(id_usuario)
    if not usuario:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios.index'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        hashed = generate_password_hash(password, method='pbkdf2:sha256') if password else usuario.password
        exito, mensaje = inv.actualizar_usuario(
            id_usuario,
            nombre=request.form['nombre'],
            email=request.form['email'],
            password=hashed
        )
        flash(mensaje, 'success' if exito else 'error')
        if exito:
            return redirect(url_for('usuarios.index'))

    return render_template('usuarios/form.html', usuario=usuario.to_dict(), accion='Editar')


@usuarios_bp.route('/eliminar/<int:id_usuario>', methods=['POST'])
@login_required
def eliminar(id_usuario):
    exito, mensaje = get_inventario().eliminar_usuario(id_usuario)
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('usuarios.index'))
