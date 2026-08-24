# importar flask
from flask import Flask, render_template, request, redirect, url_for

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
# crear una instancia de la aplicacion flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave-secreta-desarrollo'
# definir las rutas
@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/productos', methods=['GET', 'POST'])
def productos():

    form = ProductoForm()

    productos = [
        {
            "nombre": "Computadora portátil",
            "categoria": "Computación",
            "precio": 850.00,
            "stock": 5
        },
        {
            "nombre": "Teclado inalámbrico",
            "categoria": "Accesorios",
            "precio": 35.00,
            "stock": 10
        },
        {
            "nombre": "Mouse inalámbrico",
            "categoria": "Accesorios",
            "precio": 20.00,
            "stock": 0
        }
    ]

    if form.validate_on_submit():

        nuevo_producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data
        }

        productos.append(nuevo_producto)

        return redirect(url_for('productos'))

    return render_template(
        'productos.html',
        productos=productos,
        form=form
    )

# ruta de clientes
@app.route('/clientes')
def clientes():
    
    clientes = [
        {
            "nombre": "María González",
            "correo": "maria@email.com",
            "telefono": "0991111111"
        },
        {
            "nombre": "Juan Pérez",
            "correo": "juan@email.com",
            "telefono": "0982222222"
        },
        {
            "nombre": "Ana Rodríguez",
            "correo": "ana@email.com",
            "telefono": "0973333333"
        }
    ]

    return render_template(
        'clientes.html',
        clientes=clientes
    )

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():

    form = ProveedorForm()

    proveedores = [
        {
            "nombre": "Tech Ecuador",
            "contacto": "0991234567",
            "producto": "Equipos tecnológicos"
        },
        {
            "nombre": "Digital Solutions",
            "contacto": "0987654321",
            "producto": "Accesorios informáticos"
        },
        {
            "nombre": "Distribuidora Nacional",
            "contacto": "0965555555",
            "producto": "Suministros de oficina"
        }
    ]

    if form.validate_on_submit():

        nuevo_proveedor = {
            "nombre": form.nombre.data,
            "contacto": form.contacto.data,
            "producto": form.producto.data
        }

        proveedores.append(nuevo_proveedor)

        return redirect(url_for('proveedores'))

    return render_template(
        'proveedores.html',
        proveedores=proveedores,
        form=form
    )
# ruta de facturación
@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():

    form = FacturacionForm()

    facturas = [
        {
            "numero": "FAC-001",
            "cliente": "María González",
            "total": 150.00
        },
        {
            "numero": "FAC-002",
            "cliente": "Juan Pérez",
            "total": 275.50
        },
        {
            "numero": "FAC-003",
            "cliente": "Ana Rodríguez",
            "total": 89.99
        }
    ]

    if form.validate_on_submit():

        nueva_factura = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "total": form.total.data
        }

        facturas.append(nueva_factura)

        return redirect(url_for('facturacion'))

    return render_template(
        'facturacion.html',
        facturas=facturas,
        form=form
    )
if __name__ == '__main__':
    app.run(debug=True)