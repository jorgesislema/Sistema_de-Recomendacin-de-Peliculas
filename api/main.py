#Importamos las bibliotecas ausar

from fastapi import FastAPI
import pandas as pd
import numpy as np
import joblib
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA  
import re

# Definimos las rutas que bamos a usar
ruta_modelo = "C:/Users/jrgsi/OneDrive/Escritorio/PROUECTOS HENRY/SISTEMA DE RECOMENDACION PELICULAS/modelo/modelo_recomendacion_pca.pkl"
ruta_titulos = "C:/Users/jrgsi/OneDrive/Escritorio/PROUECTOS HENRY/SISTEMA DE RECOMENDACION PELICULAS/modelo/titulos.pkl"
ruta_pca = "C:/Users/jrgsi/OneDrive/Escritorio/PROUECTOS HENRY/SISTEMA DE RECOMENDACION PELICULAS/modelo/pca_model.pkl"
ruta_datos = "C:/Users/jrgsi/OneDrive/Escritorio/PROUECTOS HENRY/SISTEMA DE RECOMENDACION PELICULAS/datos/data_peliculas.csv"
ruta_datos_reducido = "C:/Users/jrgsi/OneDrive/Escritorio/PROUECTOS HENRY/SISTEMA DE RECOMENDACION PELICULAS/datos/data_peliculas_reducido.csv"

# Definimos columnas que se usan en el entrenamiento
columnas_numericas_y_genero = [
    'popularidad', 'promedio_votos', 'presupuesto', 'ingresos', 'porcentage_ganancias',
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Fantasy',
    'Horror', 'Mystery', 'Romance', 'Science Fiction', 'Thriller', 'War'
]

# Intentamos cargar los datos de entrenamiento y el modelo
try:
    df = pd.read_csv(ruta_datos_reducido)
    movie_features = df[columnas_numericas_y_genero].fillna(0)

    # Creamos el modelo PCA y reducimos las dimensiones
    n_componentes = min(30, movie_features.shape[1])
    pca = PCA(n_components=n_componentes)
    movie_features_reducido = pca.fit_transform(movie_features)

    # Guardamos el modelo en un .pkl  para futuras recomendaciones
    joblib.dump(pca, ruta_pca)

    # Creamos el modelo de recomendación 
    nbrs = NearestNeighbors(n_neighbors=6, metric='cosine').fit(movie_features_reducido)
    joblib.dump(nbrs, ruta_modelo)
    joblib.dump(df['titulo'], ruta_titulos)
    print("Modelo, PCA y títulos guardados correctamente.")
except Exception as e:
    print(f"Error durante la creación o guardado del modelo: {e}")

# Cargamos el dataset completo para la API
dataset = pd.read_csv(ruta_datos)
dataset['fecha_estreno'] = pd.to_datetime(dataset['fecha_estreno'], errors='coerce')

# Creamos las columnas de mes y día en español 
meses_es = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

dataset['mes_estreno'] = dataset['fecha_estreno'].dt.month.apply(lambda x: meses_es[int(x)-1] if pd.notna(x) else None)
dataset['dia_estreno'] = dataset['fecha_estreno'].dt.dayofweek.apply(lambda x: dias_es[int(x)] if pd.notna(x) else None)

# Cargamos el modelo de recomendación, los títulos y el PCA
try:
    modelo_recomendacion = joblib.load(ruta_modelo)
    titulos = joblib.load(ruta_titulos)
    pca = joblib.load(ruta_pca)
    print("Modelo, PCA y títulos cargados correctamente.")
except FileNotFoundError:
    modelo_recomendacion = None
    titulos = None
    pca = None
    print("Error: No se pudo cargar el modelo de recomendación, PCA o los títulos.")

# Creamos la instancia de FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API del sistema de recomendación de películas"}

# Función para la cantidad de filmaciones por mes , permite a los usuarios ingresar un mes y obtener la cantidad de películas estrenadas en ese mes. 
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    try:
        peliculas_mes = dataset[dataset['mes_estreno'].str.lower() == mes.lower()]
        cantidad = len(peliculas_mes)
        return {"mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes}"}
    except Exception as e:
        return {"error": str(e)}

# Función para la cantidad de filmaciones por día ,los usuarios pueden ingresar un día y les decimos cuántas películas se estrenaron ese día. 
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    try:
        peliculas_dia = dataset[dataset['dia_estreno'].str.lower() == dia.lower()]
        cantidad = len(peliculas_dia)
        return {"mensaje": f"{cantidad} películas fueron estrenadas en día {dia}"}
    except Exception as e:
        return {"error": str(e)}

# Función para obtener el score de una película por título ,permite a los usuarios ingresar el título de una película para obtener su año de lanzamiento y puntuación
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):
    filmacion = dataset[dataset['titulo'].str.lower() == titulo.lower()]
    if filmacion.empty:
        return {"mensaje": f"No se encontró la película {titulo}"}

    filmacion_info = filmacion.iloc[0]
    return {
        "mensaje": f"La película {filmacion_info['titulo']} fue estrenada en el año {filmacion_info['fecha_estreno'].year} con un score de {filmacion_info['promedio_votos']}"
    }

# Función para verificar si una película tiene al menos 2000 valoraciones ,si tiene 2000 votos o más, devolvemos su título, número de votos y puntuación promedio.
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    filmacion = dataset[dataset['titulo'].str.lower() == titulo.lower()]
    if filmacion.empty:
        return {"mensaje": f"No se encontró la película {titulo}"}

    filmacion_info = filmacion.iloc[0]
    if filmacion_info.get('cantidad_votos', 0) >= 2000:
        return {
            "titulo": filmacion_info['titulo'],
            "cantidad_votos": filmacion_info['cantidad_votos'],
            "promedio_votos": filmacion_info['promedio_votos']
        }
    else:
        return {"mensaje": f"La película {titulo} no cumple con el mínimo de 2000 valoraciones"}

# Función para obtener el éxito de un director basado en el retorno ,devulve un mensaje con el éxito del director y la lista de sus películas. 
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    director_films = dataset[dataset['director'].str.contains(nombre_director, case=False, na=False)]
    if director_films.empty:
        return {"mensaje": f"No se encontró al director {nombre_director}"}

    retorno_total = director_films['porcentage_ganancias'].sum()
    peliculas_info = []
    for _, row in director_films.iterrows():
        peliculas_info.append({
            "titulo": row['titulo'],
            "fecha_lanzamiento": row['fecha_estreno'],
            "retorno": row['porcentage_ganancias'],
            "presupuesto": row['presupuesto'],
            "ingresos": row['ingresos']
        })

    return {
        "mensaje": f"El director {nombre_director} tiene éxito medido por sus películas.",
        "retorno_total": retorno_total,
        "peliculas": peliculas_info
    }

# Función para obtener el éxito de un actor ,proporciona información sobre las películas de un actor y su éxito. 
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    # Verificamos si la columna 'nombre_actor' existe en el dataset
    if 'nombre_actor' not in dataset.columns:
        return {"error": "La columna 'nombre_actor' no existe en el dataset."}

    # funcion para manejar múltiples actores por película
    def actor_en_pelicula(actores):
        if pd.isna(actores):
            return False
        lista_actores = [actor.strip().lower() for actor in re.split(',|\|', actores)]
        return nombre_actor.lower() in lista_actores
    actor_films = dataset[dataset['nombre_actor'].apply(actor_en_pelicula)]

    if actor_films.empty:
        return {"mensaje": f"No se encontró al actor {nombre_actor}"}

    # Calculamos las estadísticas
    cantidad_peliculas = len(actor_films)
    retorno_total = actor_films['porcentage_ganancias'].sum()
    retorno_promedio = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    return {
        "mensaje": f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas.",
        "retorno_total": retorno_total,
        "retorno_promedio": retorno_promedio
    }

# Función para obtener recomendaciones de películas ,usamos el modelo Vecinos más cercanos para buscar películas similares.
#devuelve distancias e índices de los vecinos más cercanos
def recomendacion(titulo: str, num_recomendaciones: int = 5):
    if modelo_recomendacion is None or titulos is None or pca is None:
        return {"error": "El modelo de recomendación, PCA o los títulos no están cargados."}

    if titulo not in df['titulo'].values:
        return {"mensaje": f"La película '{titulo}' no se encuentra en el catálogo."}

    idx_pelicula = df[df['titulo'] == titulo].index[0]
    pelicula_features = df.loc[idx_pelicula, columnas_numericas_y_genero].fillna(0).values.reshape(1, -1)
    pelicula_features_reducido = pca.transform(pelicula_features)

    try:
        _, indices = modelo_recomendacion.kneighbors(pelicula_features_reducido)
        recomendaciones = titulos.iloc[indices[0][1:num_recomendaciones+1]].tolist()

        return {
            "mensaje": f"Películas recomendadas para '{titulo}':",
            "recomendaciones": recomendaciones
        }
    except Exception as e:
        return {"error": f"Error al obtener recomendaciones: {str(e)}"}
