from flask import Flask, render_template, request, redirect, url_for, flash
import os
from inventario import Inventario
from models import Producto, Cliente

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_2026'  # Necesario para flash messages

# Inicializar el sistema de inventario con POO y SQLite
inventario = Inventario()

# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def inicio():
    """Página principal con estadísticas del inventario"""
    estadisticas = inventario.obtener_estadisticas()
    productos = inventario.obtener_todos_productos()
    clientes = inventario.obtener_todos_clientes()
    facturas = inventario.obtener_todas_facturas()
    
    return render_template('index.html',
                         total_productos=len(productos),
                         total_clientes=len(clientes),
                         total_facturas=len(facturas),
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
            codigo=request.form['codigo'],
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock']),
            ubicacion=request.form['ubicacion'],
            descripcion=request.form['descripcion']
        )
        
        exito, mensaje = inventario.agregar_producto(producto)
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('productos'))
        else:
            flash(mensaje, 'error')
    
    categorias = inventario.obtener_categorias()
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
            codigo=request.form['codigo'],
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock']),
            ubicacion=request.form['ubicacion'],
            descripcion=request.form['descripcion']
        )
        
        if exito:
            flash(mensaje, 'success')
            return redirect(url_for('productos'))
        else:
            flash(mensaje, 'error')
    
    categorias = inventario.obtener_categorias()
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

@app.route('/item/<codigo>')
def item(codigo):
    """Detalle de un producto específico"""
    producto = inventario.obtener_producto_por_codigo(codigo)
    
    if producto:
        return render_template('item_detalle.html', 
                             codigo=codigo, 
                             producto=producto.to_dict())
    else:
        flash(f"Producto con código {codigo} no encontrado", 'error')
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
    facturas_list = inventario.obtener_todas_facturas()
    facturas_dict = []
    
    for factura in facturas_list:
        factura_dict = factura.to_dict()
        factura_dict['cliente'] = factura.cliente_nombre
        facturas_dict.append(factura_dict)
    
    return render_template('facturas.html', facturas=facturas_dict)

# ==================== RUTA ACERCA DE ====================

@app.route('/about')
def about():
    """Página de información del sistema"""
    return render_template('about.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
