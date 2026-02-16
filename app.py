from flask import Flask

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return "Bienvenido al Sistema de Inventario – Ferretería Wisuma"

# Ruta dinámica
@app.route('/item/<codigo>')
def item(codigo):
    return f"Item código {codigo} – Disponible en bodega."

if __name__ == '__main__': 
    app.run(debug=True, port=5001)
