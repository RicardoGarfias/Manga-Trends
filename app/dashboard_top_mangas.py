import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from database.connection import conectar

# Conexión a MySQL y lectura de datos
conn = conectar()
query = """
SELECT titulo, autor, puntaje, editorial
FROM mangatrends.manga
WHERE puntaje IS NOT NULL
"""
df = pd.read_sql(query, conn)
conn.close()

# Acortar títulos largos
df["titulo_corto"] = df["titulo"].apply(lambda x: x if len(x) <= 25 else x[:22] + "...")

# Crear app Dash
app = Dash(__name__, title="Dashboard por Puntaje")
app.layout = html.Div(
    style={"backgroundColor": "#1a1a1a", "color": "white", "fontFamily": "Arial", "padding": "20px"},
    children=[
        html.H1("Dashboard por Puntaje", style={"textAlign": "center", "marginBottom": "20px"}),
        html.Div([
            html.Label("Selecciona el rango de puntaje:", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="puntaje-slider",
                min=0,
                max=5,
                step=0.1,
                marks={i: str(i) for i in range(6)},
                value=[4.0, 5.0],
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"marginBottom": "30px"}),

        dcc.Graph(id="grafico-puntaje")
    ]
)

@app.callback(
    Output("grafico-puntaje", "figure"),
    Input("puntaje-slider", "value")
)
def actualizar_grafico(rango):
    min_score, max_score = rango
    filtrado = df[(df["puntaje"] >= min_score) & (df["puntaje"] <= max_score)]
    top_10 = filtrado.sort_values(by="puntaje", ascending=False).head(10)

    fig = px.bar(
        top_10,
        x="titulo_corto",
        y="puntaje",
        color="editorial",
        labels={"titulo_corto": "Título", "puntaje": "Puntaje"},
        title=f"Top 10 Mangas con Puntaje entre {min_score:.1f} y {max_score:.1f}"
    )
    fig.update_layout(
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#1a1a1a",
        font_color="white"
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
