from flask import Flask
import os

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
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
