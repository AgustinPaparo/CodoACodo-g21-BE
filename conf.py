import os
import psycopg2
from flask import g
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos usando variables de entorno
DATABASE_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DATABASE"),
    "port": os.getenv("DB_PORT", 5432),
}


# Función para obtener la conexión a la base de datos
def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(**DATABASE_CONFIG)
    return g.db


# Función para cerrar la conexión a la base de datos
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Función para inicializar la aplicación con el manejo de la base de datos
def init_app(app):
    app.teardown_appcontext(close_db)


def test_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    conn.commit()
    cur.close()
    conn.close()


def create_table_properties():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Properties (
            id SERIAL PRIMARY KEY,
            propietario_id INT NOT NULL,
            direccion VARCHAR(255) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            habitaciones INT NOT NULL,
            banos INT NOT NULL,
            tamano DECIMAL(10, 2) NOT NULL,
            cochera BOOLEAN NOT NULL,
            precio DECIMAL(12, 2) NOT NULL,
            estado VARCHAR(20) NOT NULL,
            tipo_contrato VARCHAR(50) NOT NULL,
            imagenes VARCHAR(255)[],
            CONSTRAINT chk_tipo CHECK (tipo IN ('casa', 'departamento', 'quinta')),
            CONSTRAINT chk_estado CHECK (estado IN ('disponible', 'alquilado', 'vendido')),
            CONSTRAINT chk_tipo_contrato CHECK (tipo_contrato IN ('venta', 'alquiler'))
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()
