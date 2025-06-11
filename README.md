# MangaTrends Web Dashboard
https://github.com/user-attachments/assets/ecec7182-8d95-488a-8ca4-3c37a6d79503

Interfaz visual oscura y estilizada con dashboards interactivos sobre el mercado del manga, diseñada con Dash (Plotly), HTML y TailwindCSS.

## 📌 Descripción
MangaTrends es una plataforma de análisis de datos del mundo del manga. Incluye visualizaciones basadas en:

- Autores más productivos
- Editoriales con más publicaciones
- Categorías de manga por año

Este repositorio contiene la versión web con UI adaptada a estilo manga-dark, integrando un `iframe` que muestra la aplicación Dash embebida dentro de una página HTML.

## 🧰 Requisitos

- Python 3.10+
- Dash y Plotly
- MySQL Server con la base de datos `MangaTrends` activa
- TailwindCSS (usado vía CDN)

## ⚙️ Estructura del proyecto

```
MangaTrends/
├── app/                        # Dash apps (dashboard principal y modulares)
│   ├── dashboard_main.py       # App principal que integra todo
│   ├── dashboard_autores_top.py
│   ├── dashboard_editoriales_top.py
│   ├── dashboard_categorias_por_ano.py
│   ├── dashboard_tipo_publicacion.py
│   ├── dashboard_evolucion_puntaje.py
│   └── dashboard_top_mangas.py

├── database/                  # Script para cargar datos a MySQL
│   └── load_to_mysql.py

├── data/
│   ├── raw/                   # Datos crudos directo del scraping
│   │   ├── mangazenkan_digital.csv
│   │   └── mangazenkan_fisico.csv
│   └── processed/             # Datos limpios listos para MySQL
│       ├── ano.csv
│       ├── autor.csv
│       ├── categoria.csv
│       ├── editorial.csv
│       ├── formato_publicacion.csv
│       ├── manga.csv
│       ├── manga_publicacion.csv
│       ├── tipo_publicacion.csv
│       └── prepare_dataset.py

├── scraping/                 # Scripts de scraping
│   ├── browser.py
│   ├── mangazenkan_fisico.py
│   ├── mangazenkan_ebook.py
│   └── img/

├── WebDrivers/               # Driver para Selenium
│   └── chromedriver.exe

├── docs/                     # Documentación del proyecto
│   └── manual_scraping.md

├── .gitignore
├── requirements.txt
├── README.md
├── html.html                 # Página web principal (interfaz visual)
└── main.py                   # Script lanzador de dashboard + navegador
```

## 🚀 Cómo ejecutar

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/MangaTrends.git
cd MangaTrends
```

2. Activa entorno virtual y dependencias:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Inicia tu backend de Dash:
```bash
python app/dashboard_main.py
```

4. Abre `web/index.html` en tu navegador.

## 🌐 ¿Cómo desplegar en GitHub Pages?

GitHub Pages no soporta Python, pero puedes subir solo la carpeta `web/`:

1. Crea una rama `gh-pages`:
```bash
git checkout -b gh-pages
```

2. Copia solo el archivo `web/index.html` a la raíz de la rama `gh-pages`

3. Haz push:
```bash
git add .
git commit -m "Publicación de sitio"
git push origin gh-pages
```

4. En tu repositorio, ve a **Settings > Pages**, selecciona la rama `gh-pages` y la carpeta `/root`.

---

## ✨ Créditos
Desarrollado por **Ricardo Garfias** – UABC – 2024. Proyecto académico para análisis de negocios con enfoque en inteligencia de datos del sector manga.
