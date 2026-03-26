from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from inventario.usuarios import Usuario
from inventario.inventario import Inventario

auth_bp = Blueprint('auth', __name__)


def get_inventario():
    from app import inventario
    return inventario


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.inicio'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        inv = get_inventario()

        if inv.buscar_usuario_por_email(email):
            flash('El email ya está registrado.', 'error')
            return redirect(url_for('auth.registro'))

        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        usuario = Usuario(nombre=nombre, email=email, password=hashed)
        exito, mensaje = inv.agregar_usuario(usuario)

        if exito:
            flash('Registro exitoso. Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        flash(f'Error al registrar: {mensaje}', 'error')

    return render_template('auth/registro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.inicio'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        inv = get_inventario()
        usuario = inv.buscar_usuario_por_email(email)

        if usuario:
            if usuario.password.startswith('pbkdf2:sha256'):
                ok = check_password_hash(usuario.password, password)
            else:
                ok = (usuario.password == password)

            if ok:
                login_user(usuario)
                flash('Sesión iniciada exitosamente.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.inicio'))

        flash('Email o contraseña incorrectos.', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('auth.login'))
