from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector


# Conexión MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Contrasena.',
    database='MangaTrends'
)

# Consulta base por cada dashboard
def get_top_autores():
    query = '''
    SELECT au.nombre AS Autor, COUNT(mr.id_manga) AS cantidad_mangas
    FROM manga_publicacion mr
    JOIN autor au ON mr.id_autor = au.id_autor
    GROUP BY au.nombre
    ORDER BY cantidad_mangas DESC
    LIMIT 20;
    '''
    return pd.read_sql(query, conn)

def get_categoria_por_ano():
    query = '''
    SELECT a.Ano, c.nombre AS Categoria, COUNT(mr.id_manga) AS Total
    FROM manga_publicacion mr
    JOIN categoria c ON mr.id_categoria = c.id_categoria
    JOIN manga m ON mr.id_manga = m.id_manga
    JOIN ano a ON m.id_ano = a.id_ano
    GROUP BY a.Ano, c.nombre
    ORDER BY a.Ano;
    '''
    return pd.read_sql(query, conn)

def get_editoriales_top():
    query = '''
    SELECT e.nombre AS Editorial, COUNT(mr.id_manga) AS cantidad_mangas
    FROM manga_publicacion mr
    JOIN editorial e ON mr.id_editorial = e.id_editorial
    GROUP BY e.nombre
    ORDER BY cantidad_mangas DESC
    LIMIT 15;
    '''
    return pd.read_sql(query, conn)

app = Dash(__name__)


# Estilo general oscuro tipo manga
app.layout = html.Div(style={
    'backgroundColor': '#121212',
    'color': 'white',
    'padding': '20px',
    'fontFamily': 'Arial'
}, children=[
    html.H1("MangaTrends Dashboard", style={'textAlign': 'center', 'color': 'white'}),

    dcc.Dropdown(
        id='dashboard-selector',
        options=[
            {'label': 'Top Autores', 'value': 'autores'},
            {'label': 'Categorías por Año', 'value': 'categorias'},
            {'label': 'Top Editoriales', 'value': 'editoriales'},
        ],
        value='autores',
        style={
            'backgroundColor': '#2c2c2c',
            'color': 'black',
            'border': '1px solid #555',
            'width': '60%',
            'margin': 'auto',
        },
        className='dropdown-dark'
    ),

    dcc.Graph(id='dashboard-content')
])

@app.callback(
    Output('dashboard-content', 'figure'),
    Input('dashboard-selector', 'value')
)
def update_dashboard(selected):
    if selected == 'autores':
        df = get_top_autores()
        fig = px.bar(df, x='Autor', y='cantidad_mangas', title='Top 20 Autores con Más Mangas',
                     template='plotly_dark', color='cantidad_mangas', color_continuous_scale='Tealgrn')
    elif selected == 'categorias':
        df = get_categoria_por_ano()
        fig = px.bar(df, x='Ano', y='Total', color='Categoria', barmode='group',
                     title='Cantidad de Mangas por Categoría y Año', template='plotly_dark')
    elif selected == 'editoriales':
        df = get_editoriales_top()
        fig = px.pie(df, names='Editorial', values='cantidad_mangas',
                     title='Top Editoriales por Publicación', template='plotly_dark')
    else:
        fig = {}
    return fig

appp = Dash(__name__)
