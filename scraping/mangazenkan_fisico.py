
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import init_browser
import requests
import os

def obtener_detalle(navegador, url, rank, titulo):
    navegador.get(url)
    time.sleep(2)
    soup = BeautifulSoup(navegador.page_source, "html.parser")

    autor = ""
    editorial = ""
    precio = ""
    volumenes = ""
    imagen_path = ""
    categoria = ""
    placa = ""
    rating = ""

    try:
        autor_tags = soup.select('a.link-underline')
        for a in autor_tags:
            href = a.get("href", "")
            if "filter_authors=" in href:
                autor = a.text.strip()
                break
    except:
        pass

    try:
        editorial_tags = soup.select('a.link-underline')
        for a in editorial_tags:
            href = a.get("href", "")
            if "publisher=" in href:
                editorial = a.text.strip()
                break
    except:
        pass

    try:
        cat_tags = soup.select("div.tags-wrapper a.link-underline")
        categorias = [cat.text.strip() for cat in cat_tags if "/s/?category=" in cat.get("href", "")]
        if categorias:
            categoria = ", ".join(categorias)
    except:
        pass

    try:
        labels = soup.select("span.description-label")
        for label in labels:
            if "版型" in label.text:
                next_span = label.find_next_sibling("span")
                if next_span:
                    placa = next_span.text.strip()
                break
    except:
        pass

    try:
        rating_span = soup.select_one("span.larger.font-weight-bold")
        if rating_span:
            rating = rating_span.text.strip()
    except:
        pass

    try:
        boton = soup.select_one("a.label-btn span")
        if boton:
            texto_completo = boton.text.strip().replace("巻", "巻 ").replace("円", "円 ")
            partes = texto_completo.split()
            for parte in partes:
                if "巻" in parte:
                    volumenes = parte.strip()
                elif "円" in parte:
                    precio = parte.replace("円", "").replace(",", "").strip()
    except:
        pass

    try:
        img = soup.select_one("div.thumbnail-holder img")
        if img:
            img_url = img.get("src")
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            elif img_url.startswith("/"):
                img_url = "https://www.mangazenkan.com" + img_url

            os.makedirs("img/portadas", exist_ok=True)
            safe_title = "".join(c for c in titulo if c.isalnum() or c in (" ", "_")).rstrip()
            file_path = f"img/portadas/{rank.zfill(3)}_{safe_title}.jpg"

            response = requests.get(img_url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                imagen_path = file_path
    except:
        pass

    return autor, editorial, precio, volumenes, imagen_path, categoria, placa, rating

def web():
    base_url = "https://www.mangazenkan.com"
    anios = list(range(2013, 2025))
    navegador = init_browser()

    datos = {
        "Ranking": [],
        "Titulo": [],
        "Autor": [],
        "Editorial": [],
        "Precio": [],
        "Volúmenes": [],
        "URL": [],
        "Portada": [],
        "Año": [],
        "Tipo": [],
        "Categoría": [],
        "Placa": [],
        "Puntaje": []
    }

    for anio in anios:
        url = f"{base_url}/r/yearly/book/{anio}/"
        navegador.get(url)
        try:
            WebDriverWait(navegador, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-name"))
            )
        except:
            continue

        for _ in range(5):
            navegador.execute_script("window.scrollBy(0, 1500);")
            time.sleep(2)

        soup = BeautifulSoup(navegador.page_source, "html.parser")
        productos = soup.select("div.product-name")
        rankings = soup.select("p.rank-number-small")
        links = soup.select("div.thumbnail-holder a")

        for r, p, l in list(zip(rankings, productos, links))[:15]:
            titulo = p.text.strip()
            rank = r.text.strip()
            href = l["href"]
            manga_url = base_url + href
            tipo = "Físico"

            autor, editorial, precio, volumenes, imagen_path, categoria, placa, rating = obtener_detalle(navegador, manga_url, rank, titulo)

            datos["Ranking"].append(rank)
            datos["Titulo"].append(titulo)
            datos["Autor"].append(autor)
            datos["Editorial"].append(editorial)
            datos["Precio"].append(precio)
            datos["Volúmenes"].append(volumenes)
            datos["URL"].append(manga_url)
            datos["Portada"].append(imagen_path)
            datos["Año"].append(anio)
            datos["Tipo"].append(tipo)
            datos["Categoría"].append(categoria)
            datos["Placa"].append(placa)
            datos["Puntaje"].append(rating)

    df = pd.DataFrame(datos)
    df.to_csv("../data/raw/mangazenkan_fisico.csv", index=False, encoding="utf-8-sig")
    navegador.quit()

if __name__ == "__main__":
    web()
