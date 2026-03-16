from flask import Flask, render_template, request, redirect, url_for, flash
import os
from inventario.database import db # Import db from its own module

import sys
import os
# Agregar carpeta Conexión al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Conexión'))
from conexion import configurar_app

def create_app():
    app = Flask(__name__)
    configurar_app(app) # Usa la configuración de MySQL definida en conexion.py
    app.secret_key = 'tu_clave_secreta_aqui_2026'

    db.init_app(app)

    return app

app = create_app()

from inventario.productos import Producto
from inventario.clientes import Cliente # Temporary import for now
from inventario.usuarios import Usuario
from inventario.inventario import Inventario
from sqlalchemy.exc import OperationalError

with app.app_context():
    try:
        # Intenta conectar a MySQL y crear tablas si no existen
        db.create_all()
        print("Tablas verificadas en la base de datos MySQL.")
    except OperationalError as e:
        print("====== ERROR DE CONEXIÓN ======")
        print("No se pudo conectar a la base de datos MySQL.")
        print("Por favor, asegúrese de que el servidor MySQL (XAMPP/WAMP o nativo) está en ejecución.")
        print("Y que la base de datos 'proyecto_inventario_wisuma' está creada en MySQL.")
        print(f"Detalle: {e}")

inventario = Inventario(app, db, Producto, Cliente, Usuario=Usuario)

# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def inicio():
    """Página principal con estadísticas del inventario"""
    # TODO: Implementar obtener_estadisticas, obtener_todos_clientes, obtener_todas_facturas con SQLAlchemy
    # For now, return placeholder values
    total_productos = len(inventario.obtener_todos_productos())
    total_clientes = len(inventario.obtener_todos_clientes())

    # Obtener categorías y productos por categoría para el index
    categorias = inventario.obtener_categorias()
    productos_por_categoria = {}
    valor_total_inventario = 0

    for categoria in categorias:
        productos_en_categoria = inventario.obtener_productos_por_categoria(categoria)
        productos_por_categoria[categoria] = [p.to_dict() for p in productos_en_categoria]
        for p in productos_en_categoria:
            valor_total_inventario += p.precio * p.stock

    estadisticas = {
        "valor_total": valor_total_inventario,
        "categorias": categorias,
        "productos_por_categoria": productos_por_categoria
    }

    # Marcador de posición para total_facturas ya que el modelo aún no está implementado
    total_facturas = 0

    return render_template('index.html',
                         total_productos=total_productos,
                         total_clientes=total_clientes,
                         total_facturas=total_facturas,
                         estadisticas=estadisticas)

# ==================== RUTAS DE PRODUCTOS (CRUD) ====================

@app.route('/productos')
def productos():
    """Lista todos los productos del inventario"""
    categoria = request.args.get('categoria', '')
    busqueda = request.args.get('busqueda', '')
    
    if categoria:
        productos_list = inventario.obtener_productos_por_categoria(categoria)
    elif busqueda:
        productos_list = inventario.buscar_productos_por_nombre(busqueda)
    else:
        productos_list = inventario.obtener_todos_productos()

    categorias = inventario.obtener_categorias()

    # Convertir objetos Producto a diccionarios para las plantillas
    productos_dict = [p.to_dict() for p in productos_list]
    
    return render_template('productos.html', 
                         productos=productos_dict,
                         categorias=categorias,
                         categoria_actual=categoria,
                         busqueda_actual=busqueda)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    """Formulario para agregar un nuevo producto"""
    if request.method == 'POST':
        # Crear objeto Producto con los datos del formulario
        producto = Producto(
            # codigo=request.form['codigo'], # Removed 'codigo' as per new model
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock']),
            descripcion=request.form['descripcion']
        )
        
        exito, mensaje = inventario.agregar_producto(producto)
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('productos'))
        else:
            flash(mensaje, 'error')
    
    # categorias = inventario.obtener_categorias()
    categorias = [] # Placeholder
    return render_template('producto_form.html', 
                         producto=None, 
                         categorias=categorias,
                         accion='Agregar')

@app.route('/productos/editar/<int:producto_id>', methods=['GET', 'POST'])
def producto_editar(producto_id):
    """Formulario para editar un producto existente"""
    producto = inventario.obtener_producto_por_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos'))
    
    if request.method == 'POST':
        exito, mensaje = inventario.actualizar_producto(
            producto_id,
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock']),
            descripcion=request.form['descripcion']
        )
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('productos'))
        else:
            flash(mensaje, 'error')
    
    # categorias = inventario.obtener_categorias()
    categorias = [] # Placeholder
    return render_template('producto_form.html', 
                         producto=producto.to_dict(),
                         categorias=categorias,
                         accion='Editar')

@app.route('/productos/eliminar/<int:producto_id>', methods=['POST'])
def producto_eliminar(producto_id):
    """Elimina un producto del inventario"""
    exito, mensaje = inventario.eliminar_producto(producto_id)
    
    if exito:
        flash(mensaje, 'success')
    else:
        flash(mensaje, 'error')
    
    return redirect(url_for('productos'))

@app.route('/item/<int:producto_id>')
def item(producto_id):
    """Detalle de un producto específico"""
    producto = inventario.obtener_producto_por_id(producto_id)

    if producto:
        return render_template('item_detalle.html',
                             producto_id=producto_id,
                             producto=producto.to_dict())
    else:
        flash(f"Producto con ID {producto_id} no encontrado", 'error')
        return redirect(url_for('productos'))

# ==================== RUTAS DE CLIENTES (CRUD) ====================

@app.route('/clientes')
def clientes():
    """Lista todos los clientes"""
    clientes_list = inventario.obtener_todos_clientes()
    clientes_dict = [c.to_dict() for c in clientes_list]
    return render_template('clientes.html', clientes=clientes_dict)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def cliente_nuevo():
    """Formulario para agregar un nuevo cliente"""
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            tipo=request.form['tipo']
        )
        
        exito, mensaje = inventario.agregar_cliente(cliente)
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('clientes'))
        else:
            flash(mensaje, 'error')
    
    return render_template('cliente_form.html', cliente=None, accion='Agregar')

@app.route('/clientes/editar/<int:cliente_id>', methods=['GET', 'POST'])
def cliente_editar(cliente_id):
    """Formulario para editar un cliente existente"""
    cliente = inventario.obtener_cliente_por_id(cliente_id)
    
    if not cliente:
        flash('Cliente no encontrado', 'error')
        return redirect(url_for('clientes'))
    
    if request.method == 'POST':
        exito, mensaje = inventario.actualizar_cliente(
            cliente_id,
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            tipo=request.form['tipo']
        )
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('clientes'))
        else:
            flash(mensaje, 'error')
    
    return render_template('cliente_form.html', 
                         cliente=cliente.to_dict(),
                         accion='Editar')

@app.route('/clientes/eliminar/<int:cliente_id>', methods=['POST'])
def cliente_eliminar(cliente_id):
    """Elimina un cliente"""
    exito, mensaje = inventario.eliminar_cliente(cliente_id)
    
    if exito:
        flash(mensaje, 'success')
    else:
        flash(mensaje, 'error')
    
    return redirect(url_for('clientes'))

# ==================== RUTAS DE FACTURAS ====================

@app.route('/facturas')
def facturas():
    """Lista todas las facturas"""
    # facturas_list = inventario.obtener_todas_facturas()
    facturas_list = [
        {"id": 1, "cliente_nombre": "Cliente A", "fecha": "2026-03-01", "valor_total": 150.75},
        {"id": 2, "cliente_nombre": "Cliente B", "fecha": "2026-03-05", "valor_total": 200.00}
    ] # Placeholder con datos de ejemplo
    facturas_dict = []
    
    for factura in facturas_list:
        factura_dict = factura
        facturas_dict.append(factura_dict)
    
    return render_template('facturas.html', facturas=facturas_dict)

@app.route('/datos/txt')
def datos_txt():
    productos_cargados, mensaje = inventario.cargar_productos_txt()
    if not productos_cargados:
        flash(mensaje, 'info')
    return render_template('datos.html', data=productos_cargados, tipo='TXT')

@app.route('/datos/txt/guardar', methods=['POST'])
def guardar_txt():
    exito, mensaje = inventario.guardar_productos_txt()
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('datos_txt'))

@app.route('/datos/txt/cargar', methods=['POST'])
def cargar_txt():
    productos_cargados, mensaje = inventario.cargar_productos_txt()
    for producto_dict in productos_cargados:
        producto = Producto.from_dict(producto_dict)
        inventario.agregar_producto(producto)
    flash(mensaje, 'success')
    return redirect(url_for('datos_txt'))

@app.route('/datos/json')
def datos_json():
    productos_cargados, mensaje = inventario.cargar_productos_json()
    if not productos_cargados:
        flash(mensaje, 'info')
    return render_template('datos.html', data=productos_cargados, tipo='JSON')

@app.route('/datos/json/guardar', methods=['POST'])
def guardar_json():
    exito, mensaje = inventario.guardar_productos_json()
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('datos_json'))

@app.route('/datos/csv')
def datos_csv():
    productos_cargados, mensaje = inventario.cargar_productos_csv()
    if not productos_cargados:
        flash(mensaje, 'info')
    return render_template('datos.html', data=productos_cargados, tipo='CSV')

@app.route('/datos/csv/guardar', methods=['POST'])
def guardar_csv():
    exito, mensaje = inventario.guardar_productos_csv()
    flash(mensaje, 'success' if exito else 'error')
    return redirect(url_for('datos_csv'))

@app.route('/datos/csv/cargar', methods=['POST'])
def cargar_csv():
    productos_cargados, mensaje = inventario.cargar_productos_csv()
    for producto_dict in productos_cargados:
        producto = Producto.from_dict(producto_dict)
        inventario.agregar_producto(producto)
    flash(mensaje, 'success')
    return redirect(url_for('datos_csv'))

@app.route('/datos/json/cargar', methods=['POST'])
def cargar_json():
    productos_cargados, mensaje = inventario.cargar_productos_json()
    for producto_dict in productos_cargados:
        producto = Producto.from_dict(producto_dict)
        inventario.agregar_producto(producto)
    flash(mensaje, 'success')
    return redirect(url_for('datos_json'))

# ==================== RUTA ACERCA DE ====================

@app.route('/about')
def about():
    """Página de información del sistema"""
    return render_template('about.html')

# ==================== RUTAS DE USUARIOS ====================

@app.route('/usuarios')
def usuarios():
    """Lista todos los usuarios del sistema"""
    usuarios_list = inventario.obtener_todos_usuarios()
    usuarios_dict = [u.to_dict() for u in usuarios_list]
    return render_template('usuarios.html', usuarios=usuarios_dict)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def usuario_nuevo():
    """Formulario para agregar un nuevo usuario"""
    if request.method == 'POST':
        usuario = Usuario(
            nombre=request.form['nombre'],
            mail=request.form['mail'],
            password=request.form['password']
        )
        
        exito, mensaje = inventario.agregar_usuario(usuario)
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('usuarios'))
        else:
            flash(mensaje, 'error')
            
    return render_template('usuario_form.html', usuario=None, accion='Agregar')

@app.route('/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
def usuario_editar(id_usuario):
    """Editar un usuario existente"""
    usuario = inventario.obtener_usuario_por_id(id_usuario)
    if not usuario:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios'))
        
    if request.method == 'POST':
        exito, mensaje = inventario.actualizar_usuario(
            id_usuario,
            nombre=request.form['nombre'],
            mail=request.form['mail'],
            password=request.form['password']
        )
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('usuarios'))
        else:
            flash(mensaje, 'error')
            
    return render_template('usuario_form.html', usuario=usuario.to_dict(), accion='Editar')

@app.route('/usuarios/eliminar/<int:id_usuario>', methods=['POST'])
def usuario_eliminar(id_usuario):
    """Elimina un usuario del sistema"""
    exito, mensaje = inventario.eliminar_usuario(id_usuario)
    if exito:
        flash(mensaje, 'success')
    else:
        flash(mensaje, 'error')
    return redirect(url_for('usuarios'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
