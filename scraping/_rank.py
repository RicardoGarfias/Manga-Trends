import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def web():
    driver=ChromeDriverManager().install()
    s= Service(driver)
    opc=Options()
    opc.add_argument("--window-size=1020,1200")
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://myanimelist.net/topmanga.php?type=manga&limit=0")
    time.sleep(10)
    rank_manga={"Rank":[],"Titulo":[],"Calificacion":[],"Link":[]}
    for i in range(0, 1):
        soup = BeautifulSoup(navegador.page_source, "html.parser")
        btnNext50 = navegador.find_element(By.LINK_TEXT, "Next 50")
        btnNext50.click()
        rank = soup.find_all("td", attrs={"valign":"top"})
        for r in rank:
            if r == None:
                rank_manga["Rank"].append("No rank")
            else:
                rank_manga["Rank"].append(r.span.text)
        titulo = soup.find_all("a", attrs={"class":"hoverinfo_trigger fs14 fw-b"})
        for t in titulo:
            if t == None:
                rank_manga["Titulo"].append("No Titulo")
                rank_manga["Link"].append("No Link")
            else:
                rank_manga["Link"].append(t["href"])
                rank_manga["Titulo"].append(t.text)
        calificacion = soup.find_all("td", attrs={"class": "score ac fs14"})
        for c in calificacion:
            if c == None:
                rank_manga["Calificacion"].append("No Calificacion")
            else:
                rank_manga["Calificacion"].append(c.span.text)
    df = pd.DataFrame(rank_manga)
    df.to_csv("../DataSets/rank_manga.csv")
    print(df.tail())
    time.sleep(3)
    navegador.close()

if __name__ == "__main__":
    web()