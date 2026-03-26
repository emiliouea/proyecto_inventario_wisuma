import os
from flask import Flask
from flask_login import LoginManager
from inventario.database import db
from sqlalchemy.exc import OperationalError
from conexion.conexion import configurar_app

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'


@login_manager.user_loader
def load_user(user_id):
    from inventario.usuarios import Usuario
    return Usuario.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    configurar_app(app)
    app.secret_key = 'tu_clave_secreta_aqui_2026'

    db.init_app(app)
    login_manager.init_app(app)

    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.productos import productos_bp
    from routes.clientes import clientes_bp
    from routes.facturas import facturas_bp
    from routes.usuarios import usuarios_bp
    from routes.datos import datos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(datos_bp)

    return app


app = create_app()

# Importar modelos y crear instancia de Inventario
from inventario.productos import Producto
from inventario.clientes import Cliente
from inventario.usuarios import Usuario
from inventario.inventario import Inventario
from models.factura import Factura, FacturaDetalle  # noqa: registra modelos con SQLAlchemy

with app.app_context():
    try:
        db.create_all()
        print('Tablas verificadas en la base de datos.')
    except OperationalError as e:
        print(f'Error al crear tablas: {e}')

inventario = Inventario(app, db, Producto, Cliente, Usuario=Usuario)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
