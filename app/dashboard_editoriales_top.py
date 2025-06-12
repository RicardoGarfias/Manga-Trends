import pandas as pd
import plotly.express as px
from dash import dash, dcc, html
import mysql.connector

# Conexión a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Contrasena.",
    database="mangatrends"
)
query = """
SELECT 
    e.nombre AS Editorial,
    COUNT(mp.id_manga) AS cantidad_mangas
FROM manga_publicacion mp
JOIN editorial e ON mp.id_editorial = e.id_editorial
GROUP BY e.nombre
ORDER BY cantidad_mangas DESC
LIMIT 3;
"""

df = pd.read_sql(query, conn)
conn.close()

fig = px.bar(df, x="cantidad_mangas", y="Editorial", orientation='h',
             title="Top 3 Editoriales con Mayor Número de Publicaciones",
             labels={"cantidad_mangas": "Cantidad de Mangas", "Editorial": "Editorial"})

fig.update_layout(yaxis={'categoryorder':'total ascending'})

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Top Editoriales por Número de Publicaciones"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
