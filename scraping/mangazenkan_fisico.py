# mangazenkan_fisico.py
from bs4 import BeautifulSoup
import pandas as pd
import time
from browser import init_browser

def web():
    url = "https://www.mangazenkan.com/r/yearly/book/2024/"
    navegador = init_browser()
    navegador.get(url)
    time.sleep(5)

    soup = BeautifulSoup(navegador.page_source, "html.parser")

    titulos = soup.find_all("p", class_="title")
    autores = soup.find_all("p", class_="author")

    datos = {"Titulo": [], "Autor": []}
    for t, a in zip(titulos, autores):
        datos["Titulo"].append(t.text.strip())
        datos["Autor"].append(a.text.strip())

    df = pd.DataFrame(datos)
    df.to_csv("../Data/raw/mangazenkan_fisico.csv", index=False)
    print(df.head())

    navegador.quit()

if __name__ == "__main__":
    web()
