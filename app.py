# ==========================================================
# IMPORTACIONES
# ==========================================================

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

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
# CONFIGURACIÓN DE BASE DE DATOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'data' / 'sistema.db'


def obtener_conexion():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

# ==========================================================
# CREAR TABLA DE PRODUCTOS
# ==========================================================

def crear_tabla_productos():

    conn = obtener_conexion()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

crear_tabla_productos()

# ==========================================================
# CREAR TABLA DE CLIENTES
# ==========================================================

def crear_tabla_clientes():

    conn = obtener_conexion()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

crear_tabla_clientes()

# ==========================================================
# CREAR TABLA DE FACTURAS
# ==========================================================

def crear_tabla_facturas():

    conn = obtener_conexion()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            cliente TEXT NOT NULL,
            total REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

crear_tabla_facturas()

# ==========================================================
# CREAR TABLA DE PROVEEDORES
# ==========================================================

def crear_tabla_proveedores():

    conn = obtener_conexion()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT NOT NULL,
            producto TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

crear_tabla_proveedores()

# ==========================================================
# RUTA PRINCIPAL
# ==========================================================

@app.route('/')
def inicio():
    return render_template('index.html')

# ==========================================================
# PRODUCTOS - LISTAR
# ==========================================================

@app.route('/productos', methods=['GET', 'POST'])
def productos():

     conn = obtener_conexion()

     productos = conn.execute(
        'SELECT * FROM productos'
    ).fetchall()

     conn.close()

     return render_template(
        'productos.html',
        productos=productos
    )


# ==========================================================
# PRODUCTOS - REGISTRAR
# ==========================================================

@app.route('/formulario_producto', methods=['GET', 'POST'])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data
        ))

        conn.commit()
        conn.close()

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

    conn = obtener_conexion()

    producto = conn.execute(
        'SELECT * FROM productos WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if producto is None:
        return redirect(url_for('productos'))

    form = ProductoForm()

    if request.method == 'GET':

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            UPDATE productos
            SET nombre = ?, categoria = ?, precio = ?, stock = ?
            WHERE id = ?
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            id
        ))

        conn.commit()
        conn.close()

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

   
    conn = obtener_conexion()

    conn.execute(
        'DELETE FROM productos WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('productos'))


@app.route('/clientes', methods=['GET', 'POST'])
def clientes():

    conn = obtener_conexion()

    clientes = conn.execute(
        'SELECT * FROM clientes'
    ).fetchall()

    conn.close()

    form = ClienteForm()

    return render_template(
        'clientes.html',
        clientes=clientes,
        form=form
    )


# ==========================================================
# CLIENTES - REGISTRAR
# ==========================================================

@app.route('/formulario_cliente', methods=['GET', 'POST'])
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            INSERT INTO clientes (nombre, correo, telefono)
            VALUES (?, ?, ?)
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data
        ))

        conn.commit()
        conn.close()

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

    conn = obtener_conexion()

    cliente = conn.execute(
        'SELECT * FROM clientes WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if cliente is None:
        return redirect(url_for('clientes'))

    form = ClienteForm()

    if request.method == 'GET':

        form.nombre.data = cliente['nombre']
        form.correo.data = cliente['correo']
        form.telefono.data = cliente['telefono']

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            UPDATE clientes
            SET nombre = ?, correo = ?, telefono = ?
            WHERE id = ?
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data,
            id
        ))

        conn.commit()
        conn.close()

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

    conn = obtener_conexion()

    conn.execute(
        'DELETE FROM clientes WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('clientes'))

# ==========================================================
# PROVEEDORES - LISTAR
# ==========================================================

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():

    conn = obtener_conexion()

    proveedores = conn.execute(
        'SELECT * FROM proveedores'
    ).fetchall()

    conn.close()

    form = ProveedorForm()

    return render_template(
        'proveedores.html',
        proveedores=proveedores,
        form=form
    )


# ==========================================================
# PROVEEDORES - REGISTRAR
# ==========================================================

@app.route('/formulario_proveedor', methods=['GET', 'POST'])
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            INSERT INTO proveedores (nombre, contacto, producto)
            VALUES (?, ?, ?)
        """, (
            form.nombre.data,
            form.contacto.data,
            form.producto.data
        ))

        conn.commit()
        conn.close()

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

    conn = obtener_conexion()

    proveedor = conn.execute(
        'SELECT * FROM proveedores WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if proveedor is None:
        return redirect(url_for('proveedores'))

    form = ProveedorForm()

    if request.method == 'GET':

        form.nombre.data = proveedor['nombre']
        form.contacto.data = proveedor['contacto']
        form.producto.data = proveedor['producto']

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            UPDATE proveedores
            SET nombre = ?, contacto = ?, producto = ?
            WHERE id = ?
        """, (
            form.nombre.data,
            form.contacto.data,
            form.producto.data,
            id
        ))

        conn.commit()
        conn.close()

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

    conn = obtener_conexion()

    conn.execute(
        'DELETE FROM proveedores WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('proveedores'))

# ==========================================================
# FACTURACIÓN - LISTAR
# ==========================================================

@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():

    conn = obtener_conexion()

    facturas = conn.execute(
        'SELECT * FROM facturas'
    ).fetchall()

    conn.close()

    form = FacturacionForm()

    return render_template(
        'facturacion.html',
        facturas=facturas,
        form=form
    )


# ==========================================================
# FACTURACIÓN - REGISTRAR
# ==========================================================

@app.route('/formulario_facturacion', methods=['GET', 'POST'])
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            INSERT INTO facturas (numero, cliente, total)
            VALUES (?, ?, ?)
        """, (
            form.numero.data,
            form.cliente.data,
            form.total.data
        ))

        conn.commit()
        conn.close()

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

    conn = obtener_conexion()

    factura = conn.execute(
        'SELECT * FROM facturas WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if factura is None:
        return redirect(url_for('facturacion'))

    form = FacturacionForm()

    if request.method == 'GET':

        form.numero.data = factura['numero']
        form.cliente.data = factura['cliente']
        form.total.data = factura['total']

    if form.validate_on_submit():

        conn = obtener_conexion()

        conn.execute("""
            UPDATE facturas
            SET numero = ?, cliente = ?, total = ?
            WHERE id = ?
        """, (
            form.numero.data,
            form.cliente.data,
            form.total.data,
            id
        ))

        conn.commit()
        conn.close()

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

    conn = obtener_conexion()

    conn.execute(
        'DELETE FROM facturas WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('facturacion'))


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == '__main__':
    app.run(debug=True)