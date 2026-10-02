# ==========================================================
# IMPORTACIONES
# ==========================================================

from flask import Flask, render_template, request, redirect, url_for

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from psycopg2.extras import RealDictCursor

from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

from models import obtener_usuario_por_id

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from conexion.conexion import obtener_conexion


# ==========================================================
# CREAR APLICACIÓN FLASK
# ==========================================================

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave-secreta-desarrollo'

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


# ==========================================================
# RUTA PRINCIPAL
# ==========================================================

@app.route('/')
def inicio():
    return render_template('index.html')


# ==========================================================
# PRODUCTOS - LISTAR
# ==========================================================

@app.route('/productos', methods=['GET'])
@login_required
def productos():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
    SELECT
        p.id_producto AS id,
        p.nombre,
        p.categoria,
        p.precio,
        p.stock,
        pr.nombre AS proveedor
    FROM productos p
    LEFT JOIN proveedores pr
        ON p.id_proveedor = pr.id_proveedor
    ORDER BY p.id_producto
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'productos.html',
        productos=productos
    )


# ==========================================================
# PRODUCTOS - REGISTRAR
# ==========================================================

@app.route('/formulario_producto', methods=['GET', 'POST'])
@login_required
def formulario_producto():

    form = ProductoForm()

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    print("PROVEEDORES ENCONTRADOS:", proveedores)

    cursor.close()
    conn.close()

    form.proveedor.choices = [
        (proveedor['id_proveedor'], proveedor['nombre'])
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
                (nombre, categoria, precio, stock, id_proveedor)
            VALUES
                (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.proveedor.data
        ))

        conn.commit()

        cursor.close()
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
@login_required
def editar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_producto AS id,
            nombre,
            categoria,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id,))

    producto = cursor.fetchone()

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    if producto is None:
        return redirect(url_for('productos'))

    form = ProductoForm()

    form.proveedor.choices = [
        (proveedor['id_proveedor'], proveedor['nombre'])
        for proveedor in proveedores
    ]

    if request.method == 'GET':

        form.nombre.data = producto['nombre']
        form.categoria.data = producto['categoria']
        form.precio.data = producto['precio']
        form.stock.data = producto['stock']
        form.proveedor.data = producto['id_proveedor']

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.proveedor.data,
            id
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('productos'))


# ==========================================================
# CLIENTES - LISTAR
# ==========================================================

@app.route('/clientes', methods=['GET'])
@login_required
def clientes():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_cliente AS id,
            nombre,
            correo,
            telefono
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes = cursor.fetchall()

    cursor.close()
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
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, correo, telefono)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data
        ))

        conn.commit()

        cursor.close()
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
@login_required
def editar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_cliente AS id,
            nombre,
            correo,
            telefono
        FROM clientes
        WHERE id_cliente = %s
    """, (id,))

    cliente = cursor.fetchone()

    cursor.close()
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
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                correo = %s,
                telefono = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data,
            id
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM clientes
        WHERE id_cliente = %s
        """,
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('clientes'))


# ==========================================================
# PROVEEDORES - LISTAR
# ==========================================================

@app.route('/proveedores', methods=['GET'])
@login_required
def proveedores():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_proveedor AS id,
            nombre,
            contacto,
            producto
        FROM proveedores
        ORDER BY id_proveedor
    """)

    proveedores = cursor.fetchall()

    cursor.close()
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
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores (
                nombre,
                contacto,
                producto
            )
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.contacto.data,
            form.producto.data
        ))

        conn.commit()

        cursor.close()
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
@login_required
def editar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_proveedor AS id,
            nombre,
            contacto,
            producto
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    proveedor = cursor.fetchone()

    cursor.close()
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
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET
                nombre = %s,
                contacto = %s,
                producto = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.contacto.data,
            form.producto.data,
            id
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id_proveedor = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('proveedores'))


# ==========================================================
# FACTURACIÓN - LISTAR
# ==========================================================

@app.route('/facturacion', methods=['GET'])
@login_required
def facturacion():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id_factura AS id,
            f.numero,
            f.id_cliente,
            c.nombre AS cliente,
            f.total
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura
    """)

    facturas = cursor.fetchall()

    cursor.close()
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
@login_required
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (numero, id_cliente, total)
            VALUES (%s, %s, %s)
        """, (
            form.numero.data,
            form.cliente.data,
            form.total.data
        ))

        conn.commit()

        cursor.close()
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
@login_required
def editar_factura(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_factura AS id,
            numero,
            id_cliente,
            total
        FROM facturas
        WHERE id_factura = %s
    """, (id,))

    factura = cursor.fetchone()

    cursor.close()
    conn.close()

    if factura is None:
        return redirect(url_for('facturacion'))

    form = FacturacionForm()

    if request.method == 'GET':

        form.numero.data = factura['numero']
        form.cliente.data = factura['id_cliente']
        form.total.data = factura['total']

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE facturas
            SET numero = %s,
                id_cliente = %s,
                total = %s
            WHERE id_factura = %s
        """, (
            form.numero.data,
            form.cliente.data,
            form.total.data,
            id
        ))

        conn.commit()

        cursor.close()
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
@login_required
def eliminar_factura(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM facturas
        WHERE id_factura = %s
        """,
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('facturacion'))


# ==========================================================
# USUARIOS - REGISTRO
# ==========================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conn.close()

            form.usuario.errors.append(
                'El usuario ya existe.'
            )

            return render_template(
                'registro.html',
                form=form
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute("""
            INSERT INTO usuarios
                (usuario, password)
            VALUES
                (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template(
        'registro.html',
        form=form
    )


# ==========================================================
# AUTENTICACIÓN - LOGIN
# ==========================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT
                id,
                usuario,
                password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario and check_password_hash(
            usuario['password'],
            form.password.data
        ):

            from models import Usuario

            usuario_obj = Usuario(
                usuario['id'],
                usuario['usuario'],
                usuario['password']
            )

            login_user(usuario_obj)

            return redirect(url_for('dashboard'))

        form.password.errors.append(
            'Usuario o contraseña incorrectos.'
        )

    return render_template(
        'login.html',
        form=form
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route('/dashboard')
@login_required
def dashboard():

    return render_template(
        'dashboard.html'
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('login'))


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == '__main__':
    app.run(debug=True)

