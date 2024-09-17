# Movies Recommendation API

Este proyecto es una API para un sistema de recomendación de películas, desarrollado con **FastAPI**. Utiliza un sistema de recomendación basado en la similitud entre películas para recomendar hasta 5 películas similares a una película dada. También incluye otros endpoints que permiten consultar datos sobre películas, actores, directores, y análisis de datos estadísticos de películas.

## Descripción

El objetivo de esta API es proporcionar una manera eficiente de recomendar películas similares basadas en títulos introducidos por los usuarios. Utiliza la similitud de coseno en los títulos de las películas para hacer las recomendaciones. También contiene endpoints adicionales que permiten obtener información como:
- Cantidad de películas estrenadas en un mes específico.
- Cantidad de películas estrenadas en un día de la semana.
- Detalles sobre la puntuación y cantidad de votos de películas.
- Información sobre actores y directores, incluyendo métricas de éxito basadas en retorno.

## Funcionalidades

### Endpoints disponibles

1. **`/cantidad_filmaciones_mes/{mes}`**: Devuelve la cantidad de películas estrenadas en un mes dado (en español).
2. **`/cantidad_filmaciones_dia/{dia}`**: Devuelve la cantidad de películas estrenadas en un día de la semana (en español).
3. **`/score_titulo/{titulo}`**: Devuelve el título, el año de estreno y el score de una película específica.
4. **`/votos_titulo/{titulo}`**: Devuelve el título, la cantidad de votos y el promedio de votos de una película (solo si tiene al menos 2000 votos).
5. **`/get_actor/{actor}`**: Devuelve la cantidad de películas, el retorno total y el retorno promedio para un actor específico.
6. **`/get_director/{director}`**: Devuelve una lista de películas dirigidas por un director, con detalles como fecha de lanzamiento, retorno, costo y ganancia.
7. **`/recomendacion/{titulo}`**: Sistema de recomendación que devuelve una lista de 5 películas similares basadas en el título dado.

## Tecnologías Utilizadas

- **Python 3.9+**
- **FastAPI**: Framework principal para el desarrollo de la API.
- **Uvicorn**: Servidor ASGI para desplegar la API.
- **Pandas**: Para la manipulación de los datos.
- **scikit-learn**: Para el cálculo de la similitud de coseno entre las películas.
- **TfidfVectorizer**: Para vectorizar los títulos de las películas y calcular la similitud.
- **Parquet**: Formato de archivo utilizado para almacenar los datos.
