# Configuración de conexión entre Flask y MySQL

config_db = {
    'host': 'localhost',
    'usuario': 'root',
    'password': '123456',   
    'database': 'proyecto_inventario_wisuma',  
    'puerto': 3307
}

def obtener_uri_conexion():
    """Genera la URI de conexión para SQLAlchemy usando PyMySQL"""
    # Formato: mysql+pymysql://usuario:password@host:puerto/database
    return f"mysql+pymysql://{config_db['usuario']}:{config_db['password']}@{config_db['host']}:{config_db['puerto']}/{config_db['database']}"

def configurar_app(app):
    """Aplica la configuración de la base de datos a la aplicación Flask"""
    app.config['SQLALCHEMY_DATABASE_URI'] = obtener_uri_conexion()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
