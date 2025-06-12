import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import mysql.connector

# Conexión a MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Contrasena.",
    database="mangatrends"
)

# Consulta de evolución de puntaje promedio anual
query = """
SELECT 
    a.Ano,
    ROUND(AVG(m.Puntaje), 2) AS puntaje_promedio
FROM manga m
JOIN ano a ON m.id_ano = a.id_ano
GROUP BY a.Ano
ORDER BY a.Ano;
"""

df = pd.read_sql(query, conn)
conn.close()

# Crear gráfico
fig = px.line(df, x="Ano", y="puntaje_promedio", markers=True,
              title="Evolución del Puntaje Promedio Anual")

# Aplicación Dash
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard 2 - Evolución Puntaje Promedio"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
