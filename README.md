# Mobilytics

**Autor:** Edgard Iglesias Rubio

**Proyecto de Grado** - Universidad EAFIT

**Maestría en Ciencias de Datos y Analítica**

**Título:** Segmentación de ubicaciones geográficas basada en datos de movilidad para estrategias de mercadeo

## Descripción

Mobilytics es un proyecto de análisis de datos de movilidad que utiliza técnicas de clustering avanzadas (DBSCAN, K-Means, Clustering Jerárquico) para identificar y clasificar lugares geográficos según los patrones de comportamiento de sus visitantes. El objetivo principal es proporcionar insights para estrategias de mercadeo basadas en la segmentación espacial y temporal de ubicaciones.

## Estructura del Proyecto

```
Mobilytics/
├── datos/                                      # Datos de entrada
│   └── filtered_amss/                         # Datos filtrados de AMSS
│
├── 1_Exploracion_Ingenieria_Variables/        # Fase 1: PySpark (Databricks)
│   ├── 01_exploracion_inicial.ipynb
│   ├── 02_base_ubicaciones_con_metricas_visitas.ipynb
│   └── 03_feature_engineering.ipynb
│
├── 2_Modelado/                                # Fase 2: Algoritmos de Clustering
│   ├── 04_dbscan_clustering_optimized.ipynb
│   ├── 05_kmeans_place_classification.ipynb
│   ├── 06_hierarchical_spatial_clustering.ipynb
│   ├── 07_hierarchical_6clusters.ipynb        # Modelo final recomendado
│   ├── results/                               # Resultados DBSCAN
│   ├── results_optimized/                     # Resultados DBSCAN optimizado
│   ├── results_hierarchical/                  # Resultados jerárquicos k=3
│   └── results_hierarchical_k6/               # Resultados jerárquicos k=6 (final)
│
├── 3_Despliegue/                              # Fase 3: Aplicación Streamlit
│   ├── .streamlit/
│   │   └── config.toml                        # Configuración de tema
│   ├── app.py                                 # Dashboard interactivo
│
└── requirements.txt                           # Dependencias globales del proyecto
```

## Instalación y Configuración

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Cuenta Databricks Community Edition (solo para Fase 1)
- Jupyter Notebook o JupyterLab (para Fase 2)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/eiglesiasr/Mobilytics.git
cd Mobilytics
```

### Paso 2: Crear Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Este comando instalará todas las dependencias necesarias:
- pandas, numpy, geopandas (procesamiento de datos)
- scikit-learn, hdbscan (algoritmos de clustering)
- dask, pyarrow, fastparquet (procesamiento paralelo)
- matplotlib, seaborn, folium (visualizaciones)
- streamlit, streamlit-folium (aplicación web)
- jupyter, ipykernel (notebooks)

## Flujo de Trabajo

### Fase 1: Exploración e Ingeniería de Variables (PySpark)

**⚠️ Importante:** Esta fase se ejecuta en **Databricks Community Edition** (gratuito)

Los notebooks de esta carpeta utilizan PySpark para el procesamiento distribuido de grandes volúmenes de datos de movilidad:

1. **01_exploracion_inicial.ipynb**: Análisis exploratorio de datos crudos
2. **02_base_ubicaciones_con_metricas_visitas.ipynb**: Agregación de métricas por ubicación
3. **03_feature_engineering.ipynb**: Creación de variables para clustering

**¿Cómo ejecutar en Databricks?**

1. Crear una cuenta gratuita en [Databricks Community Edition](https://community.cloud.databricks.com/)
2. Crear un nuevo cluster (configuración por defecto es suficiente)
3. Importar los notebooks desde la carpeta `1_Exploracion_Ingenieria_Variables/`
4. Subir los datos a DBFS (Databricks File System)
5. Ejecutar los notebooks secuencialmente

**Resultado:** Archivos CSV con features procesadas en la carpeta `datos/filtered_amss/`

### Fase 2: Modelado y Clustering (Local)

Los notebooks de clustering se ejecutan localmente con Jupyter:

```bash
jupyter notebook 2_Modelado/
```

**Notebooks disponibles:**

1. **04_dbscan_clustering_optimized.ipynb**
   - Algoritmo: DBSCAN con optimización de parámetros
   - Resultados en: `results_optimized/`

2. **05_kmeans_place_classification.ipynb**
   - Algoritmo: K-Means con método del codo y silueta
   - Clasificación de lugares por comportamiento

3. **06_hierarchical_spatial_clustering.ipynb**
   - Algoritmo: Clustering Jerárquico Aglomerativo
   - Resultados en: `results_hierarchical/` (k=3 clusters)

4. **07_hierarchical_6clusters.ipynb** ⭐ **RECOMENDADO**
   - Algoritmo: Clustering Jerárquico Aglomerativo (k=6)
   - Resultados en: `results_hierarchical_k6/`
   - **Este es el modelo final utilizado en la aplicación Streamlit**

**⚠️ Ejecutar el notebook 07 antes de lanzar la app:**

```bash
# Abrir Jupyter
jupyter notebook

# Navegar a 2_Modelado/07_hierarchical_6clusters.ipynb
# Ejecutar todas las celdas: Cell > Run All
```

Esto generará la carpeta `results_hierarchical_k6/` con los archivos necesarios:
- `hierarchical_k6_clustered_places.csv`
- `hierarchical_structure_k3_k6.csv`
- `cluster_characteristics.json`
- `hierarchical_k6_cluster_statistics.csv`

### Fase 3: Despliegue con Streamlit

**Requisito previo:** Ejecutar el notebook `07_hierarchical_6clusters.ipynb` (Fase 2)

Una vez generados los resultados del clustering jerárquico (k=6), iniciar la aplicación:

```bash
cd 3_Despliegue
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

**Características de la aplicación:**
- Visualización interactiva de clusters en mapas
- Exploración de jerarquía de clusters (k=3 → k=6)
- Estadísticas y métricas por cluster
- Filtrado y búsqueda de lugares específicos
- Análisis de características de visitantes

## Características Principales

### Algoritmos de Clustering

- **DBSCAN**: Detección de clusters basada en densidad espacial
  - Identifica clusters de forma arbitraria
  - Maneja ruido y outliers
  - No requiere especificar k a priori

- **K-Means**: Particionamiento en k clusters
  - Rápido y eficiente
  - Útil para clasificación de lugares
  - Requiere selección de k óptimo

- **Clustering Jerárquico Aglomerativo**: Estructura jerárquica de clusters
  - Permite exploración multi-nivel (k=3, k=6)
  - Basado en distancia espacial (haversine)
  - Dendrogramas para visualización de jerarquía

### Métricas de Evaluación

- **Silhouette Score**: Coherencia intra-cluster vs separación inter-cluster
- **Davies-Bouldin Index**: Compacidad y separación de clusters
- **Calinski-Harabasz Index**: Varianza entre clusters vs varianza intra-cluster
- **Coherencia Espacial**: Validación geográfica de clusters

### Visualizaciones

- Mapas interactivos con Folium
- Dendrogramas jerárquicos
- Análisis de componentes principales (PCA)
- Perfiles demográficos por cluster
- Heatmaps de correlación de features

## Dependencias Principales

### Procesamiento de Datos
- `pandas>=2.1.0`: Manipulación de datos tabulares
- `numpy>=1.26.0`: Computación numérica
- `geopandas>=0.14.0`: Análisis geoespacial
- `dask[dataframe]>=2024.0.0`: Procesamiento paralelo
- `pyarrow>=22.0.0`: Formato columnar eficiente
- `fastparquet>=2024.0.0`: Lectura/escritura Parquet

### Machine Learning
- `scikit-learn>=1.3.0`: Algoritmos de clustering
- `hdbscan>=0.8.0`: DBSCAN jerárquico optimizado

### Visualización
- `matplotlib>=3.8.0`: Gráficos estáticos
- `seaborn>=0.13.0`: Visualizaciones estadísticas
- `folium>=0.15.0`: Mapas interactivos

### Análisis Geoespacial
- `shapely>=2.0.0`: Geometrías y operaciones espaciales

### Aplicación Web
- `streamlit>=1.29.0`: Framework de dashboards
- `streamlit-folium>=0.15.0`: Integración Folium-Streamlit

### Notebooks
- `jupyter>=1.0.0`: Entorno de notebooks
- `ipykernel>=6.25.0`: Kernel de Python
- `nbformat>=5.9.0`: Formato de notebooks

### Utilidades
- `tqdm>=4.66.0`: Barras de progreso

## Resultados Esperados

El proyecto genera diferentes niveles de segmentación:

1. **Nivel 1 (k=3)**: Macro-segmentación de zonas
   - Alta densidad comercial
   - Zonas residenciales
   - Áreas mixtas

2. **Nivel 2 (k=6)**: Micro-segmentación detallada
   - Clusters específicos por perfil de visitante
   - Patrones temporales diferenciados
   - Características demográficas particulares

## Aplicaciones

- **Marketing Geolocalizado**: Identificación de zonas óptimas para campañas
- **Ubicación de Negocios**: Selección de puntos estratégicos basados en flujo de personas
- **Análisis de Competencia**: Comprensión de patrones en diferentes zonas
- **Planificación Urbana**: Insights sobre movilidad y uso del espacio


**Edgard Iglesias Rubio**
Universidad EAFIT - Maestría en Ciencias de Datos y Analítica
GitHub: [@eiglesiasr](https://github.com/eiglesiasr)
