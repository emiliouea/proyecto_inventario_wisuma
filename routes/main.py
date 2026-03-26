from flask import Blueprint, render_template
from flask_login import login_required
from models.factura import Factura

main_bp = Blueprint('main', __name__)


def get_inventario():
    from app import inventario
    return inventario


@main_bp.route('/')
@login_required
def inicio():
    inv = get_inventario()
    total_productos = len(inv.obtener_todos_productos())
    total_clientes = len(inv.obtener_todos_clientes())
    categorias = inv.obtener_categorias()

    productos_por_categoria = {}
    valor_total = 0
    for cat in categorias:
        prods = inv.obtener_productos_por_categoria(cat)
        productos_por_categoria[cat] = [p.to_dict() for p in prods]
        for p in prods:
            valor_total += p.precio * p.stock

    try:
        total_facturas = Factura.query.count()
    except Exception:
        total_facturas = 0

    estadisticas = {
        'valor_total': valor_total,
        'categorias': categorias,
        'productos_por_categoria': productos_por_categoria
    }

    return render_template('index.html',
                           total_productos=total_productos,
                           total_clientes=total_clientes,
                           total_facturas=total_facturas,
                           estadisticas=estadisticas)


@main_bp.route('/about')
def about():
    return render_template('about.html')
