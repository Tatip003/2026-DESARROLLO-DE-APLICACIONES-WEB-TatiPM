import mysql.connector


def obtener_conexion():
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='3333m',
        database='sis_ventas'
    )

    return conexion