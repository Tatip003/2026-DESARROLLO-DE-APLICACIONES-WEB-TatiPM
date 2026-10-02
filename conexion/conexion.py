import psycopg2


def obtener_conexion():
    conexion = psycopg2.connect(
        host='localhost',
        port='5432',
        user='postgres',
        password='3333t',
        database='sis_ventas'
    )

    return conexion
