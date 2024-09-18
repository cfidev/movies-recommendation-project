# Movies Recommendation Project

Este es un proyecto de recomendación de películas basado en un modelo de machine learning utilizando **FastAPI** como backend y **scikit-learn** para el modelo de recomendación. El sistema de recomendación sugiere películas similares basándose en la similitud de los títulos y otras características de las películas.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- **app**: Contiene la lógica de la API construida con FastAPI.
- **data**: Contiene el archivo `movies_dataset.parquet` con los datos de las películas.
- **notebooks**: Contiene los notebooks para análisis exploratorio de datos (EDA) y otras tareas de preprocesamiento.
- **main.py**: El archivo principal que define los endpoints de la API.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar el proyecto.

## Funcionalidades Principales

El proyecto incluye los siguientes endpoints:

1. **GET** `/cantidad_filmaciones_mes/{mes}`:
   - Devuelve la cantidad de películas estrenadas en el mes dado en español.
   - Ejemplo: `/cantidad_filmaciones_mes/julio`

2. **GET** `/cantidad_filmaciones_dia/{dia}`:
   - Devuelve la cantidad de películas estrenadas en un día específico de la semana en español.
   - Ejemplo: `/cantidad_filmaciones_dia/lunes`

3. **GET** `/score_titulo/{titulo}`:
   - Devuelve el score de una película específica, el año de estreno y el nombre.
   - Ejemplo: `/score_titulo/Toy Story`

4. **GET** `/votos_titulo/{titulo}`:
   - Devuelve la cantidad de votos y el promedio de votos de una película, si tiene al menos 2000 valoraciones.
   - Ejemplo: `/votos_titulo/Jumanji`

5. **GET** `/get_actor/{actor}`:
   - Simula la información de un actor, devolviendo la cantidad de películas en las que ha participado, retorno total y promedio.
   - Ejemplo: `/get_actor/actor`

6. **GET** `/get_director/{director}`:
   - Simula la información de un director, devolviendo una lista de películas con su respectiva fecha de lanzamiento, retorno, costo y ganancia.
   - Ejemplo: `/get_director/director`

7. **GET** `/recomendacion/{titulo}`:
   - Devuelve una lista de 5 películas similares a la ingresada utilizando un modelo de recomendación basado en similitud de títulos.
   - Ejemplo: `/recomendacion/Toy Story`

## Análisis Exploratorio de Datos (EDA)

El EDA se ha realizado utilizando **Pandas**, **Seaborn** y **Matplotlib**. El análisis incluye:

- Chequeo de valores nulos.
- Chequeo de duplicados.
- Tipos de datos.
- Análisis estadístico.
- Visualización de distribuciones de variables clave como `budget`, `revenue`.
- Análisis de correlación entre variables numéricas.
- Visualización de correlaciones multivariadas mediante `pairplot`.

Los detalles del análisis pueden encontrarse en el notebook ubicado en la carpeta `notebooks`.

## Modelo de Recomendación

El sistema de recomendación está basado en la similitud de coseno entre los títulos de las películas. Utilicé `TfidfVectorizer` para convertir los títulos en una representación numérica y luego calculamos la similitud utilizando `cosine_similarity`.

## Requerimientos

El archivo `requirements.txt` contiene todas las dependencias necesarias para ejecutar este proyecto. Algunas de las principales son:

- `fastapi`
- `uvicorn`
- `pandas`
- `scikit-learn`
- `seaborn`
- `matplotlib`

## Acceso del proyecto en Render

https://movies-recommendation-project-ucon.onrender.com/docs
