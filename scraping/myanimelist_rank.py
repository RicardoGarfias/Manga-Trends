# myanimelist_rank.py
import time
import pandas as pd
from bs4 import BeautifulSoup
from browser import init_browser  # ← Usamos el navegador compartido

def web():
    navegador = init_browser()
    navegador.get("https://myanimelist.net/topmanga.php?type=manga&limit=0")
    time.sleep(10)

    rank_manga = {"Rank": [], "Titulo": [], "Calificacion": [], "Link": []}

    soup = BeautifulSoup(navegador.page_source, "html.parser")

    rank = soup.find_all("td", attrs={"valign": "top"})
    for r in rank:
        rank_manga["Rank"].append(r.span.text if r and r.span else "No rank")

    titulo = soup.find_all("a", attrs={"class": "hoverinfo_trigger fs14 fw-b"})
    for t in titulo:
        rank_manga["Titulo"].append(t.text if t else "No Titulo")
        rank_manga["Link"].append(t["href"] if t else "No Link")

    calificacion = soup.find_all("td", attrs={"class": "score ac fs14"})
    for c in calificacion:
        rank_manga["Calificacion"].append(c.span.text if c and c.span else "No Calificacion")

    df = pd.DataFrame(rank_manga)
    df.to_csv("../Data/raw/rank_manga.csv", index=False)
    print(df.tail())

    navegador.quit()

if __name__ == "__main__":
    web()
