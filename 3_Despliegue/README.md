# Explorador de Clusters KMeans - Streamlit App

## Descripción

Aplicación interactiva de visualización de clusters KMeans para análisis de movilidad urbana en San Salvador, El Salvador.

## Características

- **4 Clusters KMeans** con objetivos estratégicos definidos:
  - **Cluster 0**: Incrementar visitas y frecuencia
  - **Cluster 1**: Fidelizar visitas ocasionales
  - **Cluster 2**: Maximizar valor por visita y presencia de marca
  - **Cluster 3**: Profundizar relación y aprovechar recurrencia

- **Visualización Interactiva**:
  - Mapa con marcadores de clusters
  - Mapa de calor
  - Filtros geográficos por área y radio
  - Filtros por tipo de lugar

- **Métricas y Estadísticas**:
  - Visitantes únicos
  - Footfall promedio por día
  - Tasa de recurrencia
  - Tiempo de estadía promedio
  - Patrones temporales (hora pico, ratios)

## Requisitos

```bash
pip install streamlit pandas folium shapely
pip install streamlit-folium==0.22.0
```

**Si hay problemas con streamlit-folium:**
```bash
# Limpiar caché de Streamlit
streamlit cache clear

# O reinstalar
pip uninstall streamlit-folium -y
pip install streamlit-folium==0.22.0
```

## Estructura de Datos

La aplicación requiere los siguientes archivos generados por el notebook `05_kmeans_place_classification.ipynb`:

```
2_Modelado/results/
├── kmeans_clustered_places.csv
└── kmeans_cluster_profiles.csv
```

## Ejecución

1. Asegúrate de haber ejecutado primero el notebook de clustering:
   ```bash
   jupyter notebook 2_Modelado/05_kmeans_place_classification.ipynb
   ```

2. Ejecuta la aplicación Streamlit:
   ```bash
   streamlit run 3_Despliegue/app.py
   ```

3. Abre tu navegador en `http://localhost:8501`

## Uso

### Panel Lateral (Configuración)

- **Modo de visualización**: Elige entre clusters con marcadores o mapa de calor
- **Filtro Geográfico**:
  - Activa/desactiva el filtro por área
  - Selecciona ubicación predefinida o coordenadas personalizadas
  - Ajusta el radio de búsqueda (0.5 - 20 km)
- **Filtrar por Clusters**: Selecciona qué clusters visualizar
- **Filtrar por tipo de lugar**: Filtra por categorías de lugares
- **Resumen de Clusters**: Estadísticas expandibles por cluster

### Panel Principal

- **Mapa Interactivo**:
  - Haz click en los marcadores para ver detalles
  - Zoom y navegación con mouse
- **Métricas Globales**: Total de lugares, clusters visibles, promedios
- **Información de Clusters**: Características y objetivos por cluster
- **Estadísticas Detalladas**: Expandibles por cluster

## Clusters y Objetivos

| Cluster | Color | Objetivo | Estrategia |
|---------|-------|----------|------------|
| 0 | 🔴 Rojo | Incrementar visitas y frecuencia | Atraer más tráfico, aumentar visibilidad |
| 1 | 🟠 Naranja | Fidelizar visitas ocasionales | Convertir visitantes ocasionales en recurrentes |
| 2 | 🟢 Verde | Maximizar valor por visita | Optimizar experiencia, aumentar tiempo de estadía |
| 3 | 🔵 Azul | Profundizar relación | Aprovechar base de usuarios leales |

## Notas

- Para mejor rendimiento, usa el filtro geográfico cuando visualices muchos lugares
- El modo mapa de calor es más eficiente para grandes volúmenes de datos
- Los datos se cachean automáticamente para mejorar la velocidad de carga
