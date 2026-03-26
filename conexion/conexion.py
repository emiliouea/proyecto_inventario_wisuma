import os

# Configuración de conexión MySQL
config_db = {
    'host': 'localhost',
    'usuario': 'root',
    'password': '123456',
    'database': 'proyecto_inventario_wisuma',
    'puerto': 3307
}


def obtener_uri_mysql():
    return (
        f"mysql+pymysql://{config_db['usuario']}:{config_db['password']}"
        f"@{config_db['host']}:{config_db['puerto']}/{config_db['database']}"
    )


def obtener_uri_sqlite():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    instance_dir = os.path.join(base_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)  # crea la carpeta si no existe
    db_path = os.path.join(instance_dir, 'inventario.db')
    return f"sqlite:///{db_path}"


def mysql_disponible():
    """Verifica si MySQL está accesible y crea la base de datos si no existe."""
    try:
        import pymysql
        # Conectar sin especificar base de datos para poder crearla
        conn = pymysql.connect(
            host=config_db['host'],
            port=config_db['puerto'],
            user=config_db['usuario'],
            password=config_db['password'],
            connect_timeout=3
        )
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{config_db['database']}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        conn.close()
        print(f"✔ Base de datos '{config_db['database']}' verificada/creada.")
        return True
    except Exception as e:
        print(f"⚠ MySQL no accesible: {e}")
        return False


def configurar_app(app):
    """Configura la URI de base de datos: MySQL si está disponible, SQLite como fallback."""
    if mysql_disponible():
        uri = obtener_uri_mysql()
        print("✔ Conectado a MySQL.")
    else:
        uri = obtener_uri_sqlite()
        print("⚠ MySQL no disponible. Usando SQLite como fallback.")

    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
