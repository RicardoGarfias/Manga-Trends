from scraping.mangafox import scrape_mangafox_top
import pandas as pd

datos = scrape_mangafox_top()
df = pd.DataFrame(datos)
print(df.head())
