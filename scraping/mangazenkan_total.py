# mangazenkan_total.py
import pandas as pd

def combinar():
    df_ebook = pd.read_csv("../DataSets/mangazenkan_ebook.csv")
    df_fisico = pd.read_csv("../DataSets/mangazenkan_fisico.csv")

    df_ebook["Tipo"] = "E-book"
    df_fisico["Tipo"] = "Físico"

    df_total = pd.concat([df_ebook, df_fisico], ignore_index=True)
    df_total.to_csv("../DataSets/mangazenkan_total.csv", index=False)
    print(df_total.head())

if __name__ == "__main__":
    combinar()
