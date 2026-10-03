import os
import psycopg2


def obtener_conexion():

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="3333t",
        database="sis_ventas"
    )

    return conexion