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

# 5. Endpoint: Información de un actor
@app.get("/get_actor/{actor}")
def get_actor(actor: str):
    actor_data = df[df['cast'].str.contains(actor, case=False, na=False)]
    
    if actor_data.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    
    cantidad_peliculas = actor_data.shape[0]
    retorno_total = actor_data['return'].sum()
    retorno_promedio = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    
    return {"actor": actor, "cantidad de películas": cantidad_peliculas, "retorno total": retorno_total, "retorno promedio": retorno_promedio}

# 6. Endpoint: Información de un director
@app.get("/get_director/{director}")
def get_director(director: str):
    director_data = df[df['crew'].str.contains(director, case=False, na=False) & (df['job'] == 'Director')]
    
    if director_data.empty:
        raise HTTPException(status_code=404, detail="Director no encontrado")
    
    resultados = []
    for _, row in director_data.iterrows():
        resultados.append({
            "película": row['title'],
            "fecha de lanzamiento": row['release_date'],
            "retorno": row['return'],
            "costo": row['budget'],
            "ganancia": row['revenue']
        })
    
    return resultados


# Limpiar los datos
df['title'] = df['title'].fillna('')
df['vote_average'] = df['vote_average'].fillna(0)
df['popularity'] = df['popularity'].fillna(0)

# Vectorizador TF-IDF para calcular la similitud de títulos
vectorizer = TfidfVectorizer(stop_words='english')

# Entrenar el vectorizador con los títulos
tfidf_matrix = vectorizer.fit_transform(df['title'])

# Calcular la matriz de similitud de coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Índice invertido para encontrar películas por título
indices = pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates()

# Endpoint de recomendación
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    # Verificar si la película existe en el dataset
    idx = indices.get(titulo.lower())
    if idx is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Calcular la similitud entre la película seleccionada y todas las demás
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordenar las películas por la similitud de coseno
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener los índices de las 5 películas más similares (excluyendo la película original)
    sim_scores = sim_scores[1:6]  # Saltar la primera, que es la película misma
    
    # Obtener los títulos de las películas similares
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = df['title'].iloc[movie_indices].tolist()
    
    return {"recomendaciones": recommended_movies}