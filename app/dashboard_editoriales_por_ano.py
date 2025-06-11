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
    password="Juanito777.",
    database="mangatrends"
)

query = """
SELECT 
    a.Ano,
    e.nombre AS Editorial,
    COUNT(*) AS cantidad
FROM manga_publicacion mp
JOIN manga m ON mp.id_manga = m.id_manga
JOIN ano a ON m.id_ano = a.id_ano
JOIN editorial e ON mp.id_editorial = e.id_editorial
GROUP BY a.Ano, e.nombre
ORDER BY a.Ano, cantidad DESC;
"""

df = pd.read_sql(query, conn)

# Gráfico interactivo
fig = px.bar(
    df,
    x="Ano",
    y="cantidad",
    color="Editorial",
    title="Editoriales con más mangas publicados por año",
    labels={"cantidad": "Cantidad de mangas", "Ano": "Año"}
)

# App de Dash
app = dash.Dash(__name__)
app.title = "Dashboard Editoriales por Año"

app.layout = html.Div([
    html.H1("Editoriales por Año", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
