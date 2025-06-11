import pandas as pd
import re

def extraer_volumenes(rango):
    if pd.isna(rango):
        return (1, 1)
    match = re.findall(r"(\d+)", str(rango))
    if len(match) == 1:
        return (int(match[0]), int(match[0]))
    elif len(match) >= 2:
        return (int(match[0]), int(match[1]))
    else:
        return (1, 1)

def prepare_dataset(fisico_path, digital_path):
    fisico_df = pd.read_csv(fisico_path)
    digital_df = pd.read_csv(digital_path)

    fisico_df["Tipo"] = "Fisico"
    digital_df["Tipo"] = "Digital"

    df = pd.concat([fisico_df, digital_df], ignore_index=True)

    df["Editorial"] = df["Editorial"].apply(lambda x: re.sub(r"\s*\(.*?\)", "", str(x)).strip())
    df["Editorial"] = df["Editorial"].fillna("Desconocido")
    df["Autor"] = df["Autor"].fillna("Desconocido")

    df["Categoria"] = df["Categoría"].replace({
        "Shōnen (manga para chicos)": "Shonen",
        "Seinen (manga para adultos)": "Seinen",
        "Shōjo (manga para chicas)": "Shojo",
        "Josei (manga para mujeres adultas)": "Josei"
    }).fillna("No clasificado")

    df["Placa"] = df["Placa"].replace("No especificado", "Sin formato").fillna("Sin formato")
    df.rename(columns={"Año": "Ano"}, inplace=True)
    df["Ano"] = df["Ano"].fillna(0)

    df[["Volumen_inicio", "Volumen_fin"]] = df["Volúmenes"].apply(lambda x: pd.Series(extraer_volumenes(x)))
    df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)
    df["Puntaje"] = pd.to_numeric(df["Puntaje"], errors="coerce").fillna(0)

    anos_df = df[["Ano"]].drop_duplicates().reset_index(drop=True)
    anos_df["id_ano"] = anos_df.index + 1
    anos_df = anos_df[["id_ano", "Ano"]]

    autores_df = df[["Autor"]].drop_duplicates().reset_index(drop=True)
    autores_df["id_autor"] = autores_df.index + 1
    autores_df = autores_df[["id_autor", "Autor"]].rename(columns={"Autor": "nombre"})

    editoriales_df = df[["Editorial"]].drop_duplicates().reset_index(drop=True)
    editoriales_df["id_editorial"] = editoriales_df.index + 1
    editoriales_df = editoriales_df[["id_editorial", "Editorial"]].rename(columns={"Editorial": "nombre"})

    categorias_df = df[["Categoria"]].drop_duplicates().reset_index(drop=True)
    categorias_df["id_categoria"] = categorias_df.index + 1
    categorias_df = categorias_df[["id_categoria", "Categoria"]].rename(columns={"Categoria": "nombre"})

    tipos_df = df[["Tipo"]].fillna("Desconocido").drop_duplicates().reset_index(drop=True)
    tipos_df["id_tipo"] = tipos_df.index + 1
    tipos_df = tipos_df[["id_tipo", "Tipo"]]

    formatos_df = df[["Placa"]].drop_duplicates().reset_index(drop=True)
    formatos_df["id_formato"] = formatos_df.index + 1
    formatos_df = formatos_df[["id_formato", "Placa"]]

    df = df.merge(anos_df, on="Ano", how="left")

    mangas_df = df[["Titulo", "id_ano", "Puntaje", "URL", "Portada", "Volumen_inicio", "Volumen_fin", "Precio"]].drop_duplicates().reset_index(drop=True)
    mangas_df["id_manga"] = mangas_df.index + 1
    mangas_df = mangas_df[["id_manga", "Titulo", "id_ano", "Puntaje", "URL", "Portada", "Volumen_inicio", "Volumen_fin", "Precio"]]

    df = df.merge(autores_df.rename(columns={"nombre": "Autor"}), on="Autor", how="left")
    df = df.merge(editoriales_df.rename(columns={"nombre": "Editorial"}), on="Editorial", how="left")
    df = df.merge(categorias_df.rename(columns={"nombre": "Categoria"}), on="Categoria", how="left")
    df = df.merge(tipos_df, on="Tipo", how="left")
    df = df.merge(formatos_df, on="Placa", how="left")
    df = df.merge(mangas_df[["Titulo", "id_ano", "id_manga"]], on=["Titulo", "id_ano"], how="left")

    relacion_df = df[["id_manga", "id_autor", "id_editorial", "id_categoria", "id_tipo", "id_formato", "Ranking"]].copy()

    autores_df.to_csv("autor.csv", index=False)
    editoriales_df.to_csv("editorial.csv", index=False)
    categorias_df.to_csv("categoria.csv", index=False)
    tipos_df.to_csv("tipo_publicacion.csv", index=False)
    formatos_df.to_csv("formato_publicacion.csv", index=False)
    anos_df.to_csv("ano.csv", index=False)
    mangas_df.to_csv("manga.csv", index=False)
    relacion_df.to_csv("manga_publicacion.csv", index=False)
    print("Archivos exportados correctamente a la carpeta 'processed'")

# Ejemplo de uso:
prepare_dataset("../raw/mangazenkan_fisico_t.csv", "../raw/mangazenkan_digital_t.csv")
