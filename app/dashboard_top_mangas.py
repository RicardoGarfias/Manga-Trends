import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import mysql.connector

# Conexión a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Juanito777.",
    database="mangatrends"
)

# Consulta SQL: Top 3 mangas por año según puntaje
query = """
SELECT *
FROM (
    SELECT 
        a.Ano,
        m.Titulo,
        m.Puntaje,
        RANK() OVER (PARTITION BY a.Ano ORDER BY m.Puntaje DESC) AS ranking
    FROM manga m
    JOIN ano a ON m.id_ano = a.id_ano
) AS sub
WHERE ranking <= 3
ORDER BY Ano, ranking;
"""

df = pd.read_sql(query, conn)
conn.close()

# Crear gráfico
fig = px.bar(df, x="Ano", y="Puntaje", color="Titulo", barmode="group",
             title="Top 3 mangas más populares por año")

# App Dash
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard 1 - Mangas Populares por Año"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
