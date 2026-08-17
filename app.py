# importar flask
from flask import Flask, render_template, request, redirect, url_for

# crear una instancia de la aplicacion flask
app = Flask(__name__)

# definir las rutas
@app.route('/')
def inicio():
    return render_template('index.html')

# ruta de producto
@app.route('/productos')
def productos():
    return render_template('productos.html')

# ruta de clientes
@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

# ruta de proveedores
@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html')

# ruta de facturacion
@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html')

if __name__ == '__main__':
    app.run(debug=True)