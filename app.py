# ==========================================================
# IMPORTACIONES
# ==========================================================

from flask import Flask, render_template, request, redirect, url_for

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


# ==========================================================
# CREAR APLICACIÓN FLASK
# ==========================================================

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave-secreta-desarrollo'


# ==========================================================
# RUTA PRINCIPAL
# ==========================================================

@app.route('/')
def inicio():
    return render_template('index.html')


# ==========================================================
# DATOS TEMPORALES DE PRODUCTOS
# ==========================================================

lista_productos = [
    {
        "id": 1,
        "nombre": "Computadora portátil",
        "categoria": "Computación",
        "precio": 850.00,
        "stock": 5
    },
    {
        "id": 2,
        "nombre": "Teclado inalámbrico",
        "categoria": "Accesorios",
        "precio": 35.00,
        "stock": 10
    },
    {
        "id": 3,
        "nombre": "Mouse inalámbrico",
        "categoria": "Accesorios",
        "precio": 20.00,
        "stock": 0
    }
]


# ==========================================================
# PRODUCTOS - LISTAR
# ==========================================================

@app.route('/productos', methods=['GET', 'POST'])
def productos():

    return render_template(
        'productos.html',
        productos=lista_productos
    )


# ==========================================================
# PRODUCTOS - REGISTRAR
# ==========================================================

@app.route('/formulario_producto', methods=['GET', 'POST'])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        nuevo_producto = {
            "id": len(lista_productos) + 1,
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data
        }

        lista_productos.append(nuevo_producto)

        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        form=form,
        editar=False
    )


# ==========================================================
# PRODUCTOS - EDITAR
# ==========================================================

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    producto = next(
        (p for p in lista_productos if p["id"] == id),
        None
    )

    if producto is None:
        return redirect(url_for('productos'))

    form = ProductoForm()

    if request.method == 'GET':

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    if form.validate_on_submit():

        producto["nombre"] = form.nombre.data
        producto["categoria"] = form.categoria.data
        producto["precio"] = form.precio.data
        producto["stock"] = form.stock.data

        return redirect(url_for('productos'))

    return render_template(
        'formulario_producto.html',
        form=form,
        editar=True
    )


# ==========================================================
# PRODUCTOS - ELIMINAR
# ==========================================================

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):

    producto = next(
        (p for p in lista_productos if p["id"] == id),
        None
    )

    if producto:
        lista_productos.remove(producto)

    return redirect(url_for('productos'))


# ==========================================================
# DATOS TEMPORALES DE CLIENTES
# ==========================================================

clientes_registrados = [
    {
        "id": 1,
        "nombre": "María González",
        "correo": "maria@email.com",
        "telefono": "0991111111"
    },
    {
        "id": 2,
        "nombre": "Juan Pérez",
        "correo": "juan@email.com",
        "telefono": "0982222222"
    },
    {
        "id": 3,
        "nombre": "Ana Rodríguez",
        "correo": "ana@email.com",
        "telefono": "0973333333"
    }
]


# ==========================================================
# CLIENTES - LISTAR Y REGISTRAR
# ==========================================================

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo_cliente = {
            "id": len(clientes_registrados) + 1,
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        clientes_registrados.append(nuevo_cliente)

        return redirect(url_for('clientes'))

    return render_template(
        'clientes.html',
        clientes=clientes_registrados,
        form=form
    )


# ==========================================================
# CLIENTES - FORMULARIO
# ==========================================================

@app.route('/formulario_cliente', methods=['GET', 'POST'])
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo_cliente = {
            "id": len(clientes_registrados) + 1,
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        clientes_registrados.append(nuevo_cliente)

        return redirect(url_for('clientes'))

    return render_template(
        'formulario_cliente.html',
        form=form,
        editar=False
    )


# ==========================================================
# CLIENTES - EDITAR
# ==========================================================

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):

    cliente = next(
        (c for c in clientes_registrados if c["id"] == id),
        None
    )

    if cliente is None:
        return redirect(url_for('clientes'))

    form = ClienteForm()

    if request.method == 'GET':

        form.nombre.data = cliente["nombre"]
        form.correo.data = cliente["correo"]
        form.telefono.data = cliente["telefono"]

    if form.validate_on_submit():

        cliente["nombre"] = form.nombre.data
        cliente["correo"] = form.correo.data
        cliente["telefono"] = form.telefono.data

        return redirect(url_for('clientes'))

    return render_template(
        'formulario_cliente.html',
        form=form,
        editar=True
    )


# ==========================================================
# CLIENTES - ELIMINAR
# ==========================================================

@app.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):

    cliente = next(
        (c for c in clientes_registrados if c["id"] == id),
        None
    )

    if cliente:
        clientes_registrados.remove(cliente)

    return redirect(url_for('clientes'))


# ==========================================================
# DATOS TEMPORALES DE PROVEEDORES
# ==========================================================

lista_proveedores = [
    {
        "id": 1,
        "nombre": "Tech Ecuador",
        "contacto": "0991234567",
        "producto": "Equipos tecnológicos"
    },
    {
        "id": 2,
        "nombre": "Digital Solutions",
        "contacto": "0987654321",
        "producto": "Accesorios informáticos"
    },
    {
        "id": 3,
        "nombre": "Distribuidora Nacional",
        "contacto": "0965555555",
        "producto": "Suministros de oficina"
    }
]


# ==========================================================
# PROVEEDORES - LISTAR Y REGISTRAR
# ==========================================================

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo_proveedor = {
            "id": len(lista_proveedores) + 1,
            "nombre": form.nombre.data,
            "contacto": form.contacto.data,
            "producto": form.producto.data
        }

        lista_proveedores.append(nuevo_proveedor)

        return redirect(url_for('proveedores'))

    return render_template(
        'proveedores.html',
        proveedores=lista_proveedores,
        form=form
    )


# ==========================================================
# PROVEEDORES - FORMULARIO
# ==========================================================

@app.route('/formulario_proveedor', methods=['GET', 'POST'])
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo_proveedor = {
            "id": len(lista_proveedores) + 1,
            "nombre": form.nombre.data,
            "contacto": form.contacto.data,
            "producto": form.producto.data
        }

        lista_proveedores.append(nuevo_proveedor)

        return redirect(url_for('proveedores'))

    return render_template(
        'formulario_proveedor.html',
        form=form,
        editar=False
    )


# ==========================================================
# PROVEEDORES - EDITAR
# ==========================================================

@app.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):

    proveedor = next(
        (p for p in lista_proveedores if p["id"] == id),
        None
    )

    if proveedor is None:
        return redirect(url_for('proveedores'))

    form = ProveedorForm()

    if request.method == 'GET':

        form.nombre.data = proveedor["nombre"]
        form.contacto.data = proveedor["contacto"]
        form.producto.data = proveedor["producto"]

    if form.validate_on_submit():

        proveedor["nombre"] = form.nombre.data
        proveedor["contacto"] = form.contacto.data
        proveedor["producto"] = form.producto.data

        return redirect(url_for('proveedores'))

    return render_template(
        'formulario_proveedor.html',
        form=form,
        editar=True
    )


# ==========================================================
# PROVEEDORES - ELIMINAR
# ==========================================================

@app.route('/eliminar_proveedor/<int:id>', methods=['POST'])
def eliminar_proveedor(id):

    proveedor = next(
        (p for p in lista_proveedores if p["id"] == id),
        None
    )

    if proveedor:
        lista_proveedores.remove(proveedor)

    return redirect(url_for('proveedores'))


# ==========================================================
# DATOS TEMPORALES DE FACTURACIÓN
# ==========================================================

lista_facturas = [
    {
        "id": 1,
        "numero": "FAC-001",
        "cliente": "María González",
        "total": 150.00
    },
    {
        "id": 2,
        "numero": "FAC-002",
        "cliente": "Juan Pérez",
        "total": 275.50
    },
    {
        "id": 3,
        "numero": "FAC-003",
        "cliente": "Ana Rodríguez",
        "total": 89.99
    }
]


# ==========================================================
# FACTURACIÓN - LISTAR Y REGISTRAR
# ==========================================================

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva_factura = {
            "id": len(lista_facturas) + 1,
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "total": form.total.data
        }

        lista_facturas.append(nueva_factura)

        return redirect(url_for('facturacion'))

    return render_template(
        'facturacion.html',
        facturas=lista_facturas,
        form=form
    )


# ==========================================================
# FACTURACIÓN - FORMULARIO
# ==========================================================

@app.route('/formulario_facturacion', methods=['GET', 'POST'])
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva_factura = {
            "id": len(lista_facturas) + 1,
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "total": form.total.data
        }

        lista_facturas.append(nueva_factura)

        return redirect(url_for('facturacion'))

    return render_template(
        'formulario_facturacion.html',
        form=form,
        editar=False
    )


# ==========================================================
# FACTURACIÓN - EDITAR
# ==========================================================

@app.route('/editar_factura/<int:id>', methods=['GET', 'POST'])
def editar_factura(id):

    factura = next(
        (f for f in lista_facturas if f["id"] == id),
        None
    )

    if factura is None:
        return redirect(url_for('facturacion'))

    form = FacturacionForm()

    if request.method == 'GET':

        form.numero.data = factura["numero"]
        form.cliente.data = factura["cliente"]
        form.total.data = factura["total"]

    if form.validate_on_submit():

        factura["numero"] = form.numero.data
        factura["cliente"] = form.cliente.data
        factura["total"] = form.total.data

        return redirect(url_for('facturacion'))

    return render_template(
        'formulario_facturacion.html',
        form=form,
        editar=True
    )


# ==========================================================
# FACTURACIÓN - ELIMINAR
# ==========================================================

@app.route('/eliminar_factura/<int:id>', methods=['POST'])
def eliminar_factura(id):

    factura = next(
        (f for f in lista_facturas if f["id"] == id),
        None
    )

    if factura:
        lista_facturas.remove(factura)

    return redirect(url_for('facturacion'))


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == '__main__':
    app.run(debug=True)