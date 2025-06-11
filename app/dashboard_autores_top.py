import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import mysql.connector


# Conexión a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Juanito777.",
    database="mangatrends"
)

query = """
SELECT 
    a.nombre AS Autor,
    COUNT(mp.id_manga) AS cantidad_mangas
FROM manga_publicacion mp
JOIN autor a ON mp.id_autor = a.id_autor
GROUP BY a.nombre
ORDER BY cantidad_mangas DESC
LIMIT 20;
"""

df = pd.read_sql(query, conn)
conn.close()

fig = px.bar(df, x="Autor", y="cantidad_mangas", title="Top 20 Autores con Más Mangas", labels={"cantidad_mangas": "Cantidad de Mangas"})
fig.update_layout(xaxis_tickangle=-45)

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Top Autores"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
