import mysql.connector
import os

# Configura tu conexión MySQL
config = {
    'user': 'root',
    'password': 'Contrasena...',
    'host': 'localhost',
    'allow_local_infile': True
}
# Ruta base donde están los archivos CSV
csv_folder = os.path.abspath(os.path.join(os.getcwd(), '..','data', 'processed'))

# Diccionario con el mapeo tabla -> archivo CSV
csv_files = {
    'ano': 'ano.csv',
    'autor': 'autor.csv',
    'categoria': 'categoria.csv',
    'editorial': 'editorial.csv',
    'tipo_publicacion': 'tipo_publicacion.csv',
    'formato_publicacion': 'formato_publicacion.csv',
    'manga': 'manga.csv',
    'manga_publicacion': 'manga_publicacion.csv'
}

# Script para crear base de datos y tablas
schema_sql = """
CREATE DATABASE IF NOT EXISTS MangaTrends CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE MangaTrends;

CREATE TABLE IF NOT EXISTS ano (
    id_ano INT PRIMARY KEY,
    Ano INT NOT NULL
);

CREATE TABLE IF NOT EXISTS autor (
    id_autor INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS editorial (
    id_editorial INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS tipo_publicacion (
    id_tipo INT PRIMARY KEY,
    Tipo VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS formato_publicacion (
    id_formato INT PRIMARY KEY,
    Placa VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS manga (
    id_manga INT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    id_ano INT,
    puntaje FLOAT,
    url TEXT,
    portada TEXT,
    volumen_inicio INT,
    volumen_fin INT,
    precio FLOAT,
    FOREIGN KEY (id_ano) REFERENCES ano(id_ano)
);

CREATE TABLE IF NOT EXISTS manga_publicacion (
    id_manga INT,
    id_autor INT,
    id_editorial INT,
    id_categoria INT,
    id_tipo INT,
    id_formato INT,
    Ranking INT,
    PRIMARY KEY (id_manga, id_autor, id_editorial, id_categoria, id_tipo, id_formato),
    FOREIGN KEY (id_manga) REFERENCES manga(id_manga),
    FOREIGN KEY (id_autor) REFERENCES autor(id_autor),
    FOREIGN KEY (id_editorial) REFERENCES editorial(id_editorial),
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),
    FOREIGN KEY (id_tipo) REFERENCES tipo_publicacion(id_tipo),
    FOREIGN KEY (id_formato) REFERENCES formato_publicacion(id_formato)
);
"""

# Conexión sin base inicial para crear todo
conn = mysql.connector.connect(
    user=config['user'],
    password=config['password'],
    host=config['host'],
    allow_local_infile=True
)
cursor = conn.cursor()

# Ejecutar script SQL completo
for statement in schema_sql.split(';'):
    stmt = statement.strip()
    if stmt:
        cursor.execute(stmt)

# Activar LOAD DATA LOCAL
cursor.execute("SET GLOBAL local_infile = 1;")

# Cambiar a la base MangaTrends explícitamente
cursor.execute("USE MangaTrends;")

# Cargar cada archivo CSV
for table, filename in csv_files.items():
    file_path = os.path.join(csv_folder, filename)
    query = f"""
        LOAD DATA LOCAL INFILE '{file_path.replace('\\', '/')}'
        INTO TABLE {table}
        FIELDS TERMINATED BY ','
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    """
    try:
        cursor.execute(query)
        print(f"Datos cargados en {table} desde {filename}")
    except Exception as e:
        print(f"Error al cargar {filename} en {table}: {e}")

conn.commit()
cursor.close()
conn.close()
