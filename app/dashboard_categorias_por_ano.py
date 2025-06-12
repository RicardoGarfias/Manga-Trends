import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import mysql.connector


# Conexión a la base de datos
# Conexión a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Contrasena.",
    database="mangatrends"
)


query = """
SELECT 
    a.Ano,
    c.nombre AS Categoria,
    COUNT(*) AS cantidad
FROM manga_publicacion mp
JOIN manga m ON mp.id_manga = m.id_manga
JOIN ano a ON m.id_ano = a.id_ano
JOIN categoria c ON mp.id_categoria = c.id_categoria
GROUP BY a.Ano, c.nombre
ORDER BY a.Ano, cantidad DESC;
"""

df = pd.read_sql(query, conn)

# Gráfico de área o líneas
fig = px.area(
    df,
    x="Ano",
    y="cantidad",
    color="Categoria",
    title="Popularidad de géneros por año",
    labels={"cantidad": "Cantidad de mangas", "Ano": "Año"}
)

# App de Dash
app = dash.Dash(__name__)
app.title = "Dashboard Géneros por Año"

app.layout = html.Div([
    html.H1("Géneros más populares por año", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
