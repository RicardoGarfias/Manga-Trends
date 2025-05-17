import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# PASO A: Configura el navegador
def configurar_navegador():
    opciones = Options()
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--disable-blink-features=AutomationControlled")
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option("useAutomationExtension", False)

    driver_path = ChromeDriverManager().install()  # Descarga el driver correcto
    service = Service(executable_path=driver_path)

    return webdriver.Chrome(service=service, options=opciones)

# PASO B: Función principal de scraping
def extraer_mangas_fisicos():
    navegador = configurar_navegador()
    url = "https://www.mangazenkan.com/r/yearly/book/2024/"
    navegador.get(url)
    time.sleep(5)  # Esperar a que cargue todo

    sopa = BeautifulSoup(navegador.page_source, "html.parser")
    navegador.quit()

    tabla = sopa.find("table", class_="ranking-table")
    filas = tabla.find("tbody").find_all("tr")

    datos = []
    for fila in filas:
        celdas = fila.find_all("td")
        if len(celdas) >= 5:
            datos.append({
                "ranking": celdas[0].text.strip(),
                "titulo": celdas[1].text.strip(),
                "autor": celdas[2].text.strip(),
                "editorial": celdas[3].text.strip(),
                "ventas": celdas[4].text.strip().replace(",", ""),
                "formato": "Físico",
                "año": 2024
            })

    df = pd.DataFrame(datos)
    df.to_csv("data/raw/manga_fisico_2024.csv", index=False, encoding="utf-8-sig")
    print(" CSV guardado: manga_fisico_2024.csv")
    return df

# PASO C: Ejecutar script
if __name__ == "__main__":
    df_mangas = extraer_mangas_fisicos()
    print(df_mangas.head())
