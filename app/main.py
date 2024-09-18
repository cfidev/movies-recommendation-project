from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os

app = FastAPI()

# Obtener la ruta absoluta del archivo Parquet
current_dir = os.path.dirname(os.path.abspath(__file__))
parquet_file_path = os.path.join(current_dir, '../data/movies_dataset.parquet')

# Cargar el archivo Parquet limpio
df = pd.read_parquet(parquet_file_path)

@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente"}

# 1. Endpoint: Cantidad de filmaciones por mes en español
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    mes_num = meses.get(mes.lower())
    if not mes_num:
        raise HTTPException(status_code=400, detail="Mes inválido")
    
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    cantidad = df[df['release_date'].dt.month == mes_num].shape[0]
    
    return {"mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes}"}

# 2. Endpoint: Cantidad de filmaciones por día en español
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
        'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    
    dia_num = dias.get(dia.lower())
    if dia_num is None:
        raise HTTPException(status_code=400, detail="Día inválido")
    
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    cantidad = df[df['release_date'].dt.weekday == dia_num].shape[0]
    
    return {"mensaje": f"{cantidad} películas fueron estrenadas en {dia}"}

# 3. Endpoint: Score y año de estreno por título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    pelicula = df[df['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    score = pelicula.iloc[0]['vote_average']
    anio = pelicula.iloc[0]['release_year']
    
    return {"título": titulo, "año de estreno": anio, "score": score}

# 4. Endpoint: Votos por título (con al menos 2000 valoraciones)
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    pelicula = df[df['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    votos = pelicula.iloc[0]['vote_count']
    if votos < 2000:
        raise HTTPException(status_code=400, detail="La película no tiene suficientes votos")
    
    promedio = pelicula.iloc[0]['vote_average']
    return {"título": titulo, "cantidad de votos": votos, "promedio de votos": promedio}

# 5. Endpoint: Información de un actor (simulado)
@app.get("/get_actor/{actor}")
def get_actor(actor: str):
    if actor.lower() == "actor":
        cantidad_peliculas = 10
        retorno_total = 5000000
        retorno_promedio = retorno_total / cantidad_peliculas
        return {"actor": actor, "cantidad de películas": cantidad_peliculas, "retorno total": retorno_total, "retorno promedio": retorno_promedio}
    
    raise HTTPException(status_code=404, detail="Actor no encontrado")

# 6. Endpoint: Información de un director (simulado)

@app.get("/get_director/{director}")
def get_director(director: str):
    if director.lower() == "director":
        resultados = [
            {
                "película": "Pelicula 1",
                "fecha de lanzamiento": "2020-01-01",
                "retorno": 1000000,
                "costo": 500000,
                "ganancia": 500000
            },
            {
                "película": "Pelicula 2",
                "fecha de lanzamiento": "2019-01-01",
                "retorno": 2000000,
                "costo": 1000000,
                "ganancia": 1000000
            }
        ]
        return resultados
    
    raise HTTPException(status_code=404, detail="Director no encontrado")


#Endpoint de recomendación
# Reemplazar valores nulos en la columna 'title'
df['title'] = df['title'].fillna('')

# Entrenamiento del modelo de recomendación
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['title'])

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    # Verificar si el título existe
    if titulo not in df['title'].values:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Calcular similitud
    idx = df[df['title'] == titulo].index[0]
    cos_similarities = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    
    # Obtener las 5 películas más similares
    similar_indices = cos_similarities.argsort()[-6:-1][::-1]  # Ignorar la propia película
    recomendaciones = df['title'].iloc[similar_indices].values.tolist()
    
    return {"recomendaciones": recomendaciones}
