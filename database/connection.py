import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_contraseña",
        database="mangatrends"
    )
