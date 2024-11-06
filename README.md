# 🎬 Proyecto Individual Nº1: Sistema de Recomendación de Películas

---

## 📌 Descripción
Este proyecto simula el entorno real de trabajo de un **Ingeniero MLOps**, permitiendo ganar experiencia práctica en el desarrollo de aplicaciones basadas en datos, desde la recolección y transformación de información hasta el despliegue de un modelo de machine learning en producción.

La API proporciona funcionalidades avanzadas, como la obtención de datos por fechas, consultas de votaciones y el cálculo de similitud entre películas para generar recomendaciones. Además, este proyecto fomenta la **adquisición de habilidades esenciales para el mundo laboral**, incluyendo el análisis de datos, el diseño de sistemas de recomendación y la implementación de soluciones escalables en la web.

Finalmente, el proyecto culmina con el despliegue de la aplicación en **Render** y la creación de un video demostrativo que valida el funcionamiento del sistema, permitiendo aplicar lo aprendido en un contexto realista y prepararse para el entorno profesional en ciencia de datos y MLOps.

---

## 📂 Estructura del Proyecto

```plaintext
proyecto_recomendacion_peliculas/
├── .vscode/                       # Configuración de VS Code (opcional)
├── api/                           # Implementación de la API
│   ├── __pycache__/               # Archivos de caché de Python generados automáticamente
│   └── main.py                    # Archivo principal para iniciar la API (FastAPI)
├── datos/                         # Almacenamiento de los datasets
│   ├── credits.csv                # Dataset original de créditos de películas
│   ├── credits_desanidado.csv     # Dataset de créditos desanidado
│   ├── data_peliculas.csv         # Dataset original de películas
│   ├── data_peliculas_reducido.csv# Versión reducida del dataset de películas
│   ├── Diccionario de Datos - PIMLO.xlsx # Diccionario de datos para referencia
│   ├── movies_dataset.csv         # Dataset original de películas
│   └── movies_dataset_desanidado.csv # Dataset de películas desanidado
├── modelo/                        # Modelo de machine learning
│   ├── modelo_recomendacion_pca.pkl # Modelo entrenado de recomendación basado en PCA
│   ├── modelo.ipynb               # Notebook para el entrenamiento del modelo
│   ├── pca_model.pkl              # Archivo guardado del modelo PCA
│   └── titulos.pkl                # Archivo de títulos de películas para recomendaciones
├── raiz/                          # Archivos de configuración de entorno
│   └── venv/                      # Entorno virtual para el proyecto
├── scripts/                       # Scripts de procesamiento y análisis de datos
│   ├── EDA.ipynb                  # Análisis Exploratorio de Datos (EDA)
│   ├── ETL credits.ipynb          # Proceso ETL de créditos
│   └── ETL movies_dataset.ipynb   # Proceso ETL del dataset de películas
└── requirements.txt               # Dependencias necesarias para el proyecto

📝 Descripción General

El sistema de recomendación de películas consta de las siguientes etapas principales:
1. ETL (Extracción, Transformación y Carga)
📥 1.1 Extracción de Datos

    Se obtuvieron los datasets movies_dataset.csv y credits.csv del repositorio proporcionado por Henry.
    Se descargó el Diccionario de Datos para entender las columnas disponibles. 

🔄 1.2 Transformación

    Se utilizó Visual Studio Code y se creó un entorno virtual para gestionar las dependencias.
    Se desarrollaron los notebooks ETL credits.ipynb y ETL movies_dataset.ipynb.
    Se desanidaron campos como belongs_to_collection y production_companies que estaban en formato de diccionario o lista.
    Transformaciones aplicadas:
        Valores nulos: Los campos revenue y budget con valores nulos se rellenaron con 0.
        Fechas faltantes: Las filas con valores nulos en release date se eliminaron.
        Formato de fecha: Se estandarizaron las fechas al formato AAAA-mm-dd.
        Año de estreno: Se creó la columna release_year extrayendo el año de la fecha de estreno.
        Retorno de inversión: Se creó la columna return calculando revenue / budget, asignando 0 cuando no había datos disponibles.
        Columnas eliminadas: Se eliminaron las columnas video, imdb_id, adult, original_title, poster_path y homepage. 

📤 1.3 Carga

    Tras la limpieza y transformación, se generaron gráficos para visualizar y comprender mejor los datos. 

2. 📊 Análisis Exploratorio de Datos (EDA)

    Se creó el notebook EDA.ipynb para realizar el análisis estadístico.
    Se identificaron y trataron valores faltantes y duplicados.
    Se unieron los datasets basados en el id de las películas.
    Se eliminaron columnas irrelevantes y se tradujeron los nombres de las columnas al español.
    Se aplicó One-Hot Encoding a los géneros, creando columnas binarias para cada género.
    Se generaron gráficos para identificar patrones y tendencias que puedan influir en el modelo de recomendación. 

3. 🚀 Desarrollo de la API

    Se desarrolló una API utilizando el framework FastAPI.
    Funcionalidades implementadas:
        Cantidad de filmaciones por mes : Permite obtener la cantidad de filmaciones registradas en un mes específico.
        Cantidad de filmaciones por día : Proporciona el número de filmaciones registradas en un día específico.
        Score de una filmación : Devuelve el puntaje asociado a una película específica.
        Cantidad de votos de una filmación : Muestra la cantidad de votos recibidos por una película.
        Obtener actor : Proporciona información sobre un actor en particular.
        Obtener director : Proporciona información sobre un director específico. 

4. 🧠 Construcción del Modelo de Recomendación

    Se utilizó el dataset data_peliculas_reducido.csv, reduciendo a 5000 películas más relevantes por cuestiones de rendimiento.
    Pasos realizados:
        Selección de características relevantes : Se seleccionaron las variables más significativas y se manejaron los valores faltantes.
        Reducción de dimensionalidad : Se aplicó PCA para reducir a un máximo de 30 componentes, simplificando los datos y manteniendo la mayor cantidad de información posible.
        Modelo de Vecinos Más Cercanos : Se utilizó Nearest Neighbors con similitud de coseno para encontrar películas similares.
        Entrenamiento y guardado del modelo : El modelo entrenado se guardó para su uso posterior sin necesidad de reentrenamiento. 

5. 🌐 Despliegue de la API

    La API se desplegó en la plataforma Render , haciéndola accesible para usuarios finales. 

6. ⚙️ Framework Utilizado

    Se empleó FastAPI para el desarrollo de la API, facilitando la construcción de servicios web basados en Python de manera rápida y sencilla. 

📦 Requisitos y Dependencias

Para ejecutar este proyecto, es necesario tener instaladas las siguientes dependencias:

annotated-types==0.7.0
anyio==4.6.2.post1
click==8.1.7
colorama==0.4.6
faiss-cpu==1.9.0
fastapi==0.115.4
h11==0.14.0
idna==3.10
joblib==1.4.2
numpy==2.1.3
packaging==24.1
pandas==2.2.3
pydantic==2.9.2
pydantic_core==2.23.4
python-dateutil==2.9.0.post0
pytz==2024.2
scikit-learn==1.5.2
scipy==1.14.1
six==1.16.0
sniffio==1.3.1
starlette==0.41.2
threadpoolctl==3.5.0
typing_extensions==4.12.2
tzdata==2024.2
uvicorn==0.32.0
#Link de render
https://proyecto-individual-n-1-sistema-de.onrender.com/docs#/default/recomendacion_recomendacion__titulo__get
