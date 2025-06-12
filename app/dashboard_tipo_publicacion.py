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
    a.Ano,
    tp.Tipo AS Tipo_Publicacion,
    COUNT(*) AS cantidad
FROM manga_publicacion mp
JOIN manga m ON mp.id_manga = m.id_manga
JOIN ano a ON m.id_ano = a.id_ano
JOIN tipo_publicacion tp ON mp.id_tipo = tp.id_tipo
GROUP BY a.Ano, tp.Tipo
ORDER BY a.Ano;
"""

df = pd.read_sql(query, conn)
conn.close()

fig = px.area(df, x="Ano", y="cantidad", color="Tipo_Publicacion",
              title="Evolución del Tipo de Publicación (Físico vs Digital)",
              labels={"cantidad": "Cantidad de Publicaciones", "Ano": "Año"})

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Evolución por Tipo de Publicación"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
