from flask import Flask, render_template
import os

app = Flask(__name__)

# Datos de ejemplo (simulando una base de datos)
productos_data = [
    {
        'codigo': 'FER001',
        'nombre': 'Martillo de Carpintero',
        'categoria': 'Herramientas',
        'precio': 15.99,
        'stock': 45,
        'ubicacion': 'Bodega A - Estante 3',
        'descripcion': 'Martillo profesional con mango de madera, ideal para trabajos de carpintería.'
    },
    {
        'codigo': 'FER002',
        'nombre': 'Destornillador Phillips',
        'categoria': 'Herramientas',
        'precio': 8.50,
        'stock': 120,
        'ubicacion': 'Bodega A - Estante 5',
        'descripcion': 'Destornillador de precisión con punta magnética.'
    },
    {
        'codigo': 'FER003',
        'nombre': 'Taladro Eléctrico',
        'categoria': 'Herramientas Eléctricas',
        'precio': 89.99,
        'stock': 12,
        'ubicacion': 'Bodega B - Estante 1',
        'descripcion': 'Taladro eléctrico de 500W con velocidad variable y reversible.'
    },
    {
        'codigo': 'FER004',
        'nombre': 'Pintura Látex Blanca',
        'categoria': 'Pinturas',
        'precio': 25.00,
        'stock': 30,
        'ubicacion': 'Bodega C - Estante 2',
        'descripcion': 'Pintura látex de alta calidad, rendimiento 12 m²/litro.'
    },
    {
        'codigo': 'FER005',
        'nombre': 'Cemento Portland',
        'categoria': 'Construcción',
        'precio': 12.50,
        'stock': 200,
        'ubicacion': 'Bodega D - Piso',
        'descripcion': 'Cemento Portland tipo I, saco de 50kg.'
    },
    {
        'codigo': 'FER006',
        'nombre': 'Cinta Métrica 5m',
        'categoria': 'Herramientas',
        'precio': 6.75,
        'stock': 80,
        'ubicacion': 'Bodega A - Estante 4',
        'descripcion': 'Cinta métrica retráctil de 5 metros con freno automático.'
    }
]

clientes_data = [
    {'id': 'CLI001', 'nombre': 'Juan Pérez', 'telefono': '555-1234', 'email': 'juan@email.com', 'tipo': 'Regular'},
    {'id': 'CLI002', 'nombre': 'María González', 'telefono': '555-5678', 'email': 'maria@email.com', 'tipo': 'Premium'},
    {'id': 'CLI003', 'nombre': 'Carlos Rodríguez', 'telefono': '555-9012', 'email': 'carlos@email.com', 'tipo': 'Regular'},
    {'id': 'CLI004', 'nombre': 'Ana Martínez', 'telefono': '555-3456', 'email': 'ana@email.com', 'tipo': 'Premium'},
]

facturas_data = [
    {'numero': 'FAC-001', 'fecha': '2026-02-15', 'cliente': 'Juan Pérez', 'total': 125.50, 'estado': 'pagado'},
    {'numero': 'FAC-002', 'fecha': '2026-02-18', 'cliente': 'María González', 'total': 89.99, 'estado': 'pagado'},
    {'numero': 'FAC-003', 'fecha': '2026-02-20', 'cliente': 'Carlos Rodríguez', 'total': 250.00, 'estado': 'pendiente'},
    {'numero': 'FAC-004', 'fecha': '2026-02-21', 'cliente': 'Ana Martínez', 'total': 45.75, 'estado': 'pagado'},
]

# Ruta principal
@app.route('/')
def inicio():
    return render_template('index.html',
                         total_productos=len(productos_data),
                         total_clientes=len(clientes_data),
                         total_facturas=len(facturas_data))

# Ruta de productos
@app.route('/productos')
def productos():
    return render_template('productos.html', productos=productos_data)

# Ruta dinámica para ver detalle de un producto
@app.route('/item/<codigo>')
def item(codigo):
    producto = next((p for p in productos_data if p['codigo'] == codigo), None)
    if producto:
        return render_template('item_detalle.html', codigo=codigo, producto=producto)
    else:
        return f"Producto con código {codigo} no encontrado.", 404

# Ruta de clientes
@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=clientes_data)

# Ruta de facturas
@app.route('/facturas')
def facturas():
    return render_template('facturas.html', facturas=facturas_data)

# Ruta "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
