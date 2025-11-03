# Explorador de Clusters Jerárquicos

Aplicación interactiva en Streamlit para explorar y analizar clusters jerárquicos de lugares en San Salvador, El Salvador.

## Características

- **Navegación Jerárquica**: Alterna entre K=3 (macro-segmentos) y K=6 (micro-segmentos)
- **Visualización Dual**:
  - Modo Clusters: Marcadores interactivos con información detallada
  - Modo Mapa de Calor: Visualización de densidad de lugares
- **Filtro Geográfico Inteligente**: 🆕
  - Filtra lugares por ubicación y radio (0.5-20 km)
  - Ubicaciones predefinidas de San Salvador
  - Coordenadas personalizadas
  - Mejora significativa del rendimiento para explorar áreas específicas
- **Filtros Interactivos**: Filtra por clusters y tipos de lugares
- **Información Detallada**: Click en marcadores para ver métricas completas
- **Árbol Jerárquico**: Visualiza la relación entre clusters K=3 y K=6
- **Optimización de Rendimiento**: Límite automático de marcadores para navegadores

## Métricas Disponibles

Para cada lugar:
- Dispositivos únicos (unique_devices_count)
- Footfall promedio por día
- Tasa de recurrencia
- Tiempo de estadía promedio
- Horas pico de actividad
- Tipo de lugar (clase)

## Instalación

### 1. Requisitos Previos

Asegúrate de haber ejecutado el notebook `07_hierarchical_6clusters.ipynb` en la carpeta `2_Modelado` para generar los datos necesarios:

- `results_hierarchical_k6/hierarchical_k6_clustered_places.csv`
- `results_hierarchical_k6/hierarchical_structure_k3_k6.csv`
- `results_hierarchical_k6/cluster_characteristics.json`
- `results_hierarchical_k6/hierarchical_k6_cluster_statistics.csv`

### 2. Instalar dependencias

```bash
cd 3_Despliegue
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Navegación

**Panel Lateral (Sidebar):**
- Selecciona el nivel de clustering (K=3 o K=6)
- Elige el modo de visualización (Clusters o Mapa de Calor)
- **Filtro Geográfico** 🆕:
  - Activa el filtro por área para mejorar rendimiento
  - Selecciona ubicaciones predefinidas o coordenadas personalizadas
  - Ajusta el radio de búsqueda (0.5-20 km)
- Filtra por clusters específicos
- Filtra por tipos de lugares
- Visualiza la estructura jerárquica completa

**Mapa Principal:**
- **Modo Clusters**: Haz click en los marcadores para ver información detallada de cada lugar
- **Modo Mapa de Calor**: Visualiza zonas de alta densidad de lugares
- Usa el zoom y pan para explorar diferentes áreas
- Los colores representan diferentes clusters

**Panel Derecho:**
- Información detallada de cada cluster seleccionado
- Estadísticas agregadas por cluster
- Top 5 tipos de lugares en cada cluster

## Estructura de Datos

La aplicación espera los siguientes archivos en `../2_Modelado/results_hierarchical_k6/`:

```
results_hierarchical_k6/
├── hierarchical_k6_clustered_places.csv   # Datos completos con clusters asignados
├── hierarchical_structure_k3_k6.csv       # Relación entre K=3 y K=6
├── cluster_characteristics.json           # Características y nombres descriptivos
└── hierarchical_k6_cluster_statistics.csv # Perfiles estadísticos de clusters
```

## Personalización

### Colores de Clusters

Los colores se definen en la función `get_cluster_color()`:
- K=3: Rojo, Azul, Verde
- K=6: Rojo, Naranja, Amarillo, Verde, Azul, Morado

### Centro del Mapa

Por defecto, el mapa está centrado en San Salvador:
- Latitud: 13.6929
- Longitud: -89.2182

Puedes modificar esto en la función `create_base_map()`.

### Radio del Heatmap

Ajusta el radio y blur del mapa de calor en `create_cluster_map()`:
```python
plugins.HeatMap(heat_data, radius=15, blur=25, max_zoom=13)
```

## Optimización de Rendimiento

### Para datasets grandes (>5,000 lugares)

La aplicación incluye varias optimizaciones para manejar grandes volúmenes de datos:

1. **Filtro Geográfico** (Recomendado):
   - Activa el filtro por área en el sidebar
   - Selecciona una ubicación de interés (ej: Centro de San Salvador)
   - Ajusta el radio según tu necesidad (recomendado: 2-5 km)
   - Esto reduce significativamente la cantidad de datos a procesar

2. **Mapa de Calor**:
   - Usa el modo "Mapa de calor" en lugar de "Clusters"
   - Ideal para visualizar patrones de densidad sin cargar marcadores individuales
   - Mucho más eficiente para áreas con alta concentración de lugares

3. **Límite Automático de Marcadores**:
   - La app limita automáticamente a 5,000 marcadores en modo clusters
   - Si hay más lugares, se mostrará una advertencia
   - Los primeros 5,000 lugares se mostrarán ordenados

### Ejemplo de uso eficiente:

```
1. Activa "Filtro por área"
2. Selecciona "Centro de San Salvador"
3. Ajusta radio a 3 km
4. Resultado: ~500-1000 lugares (carga rápida)
5. Explora detalles haciendo click en marcadores
```

## Troubleshooting

### Error: "Error cargando datos"

**Solución**: Ejecuta primero el notebook `07_hierarchical_6clusters.ipynb` para generar los archivos de datos necesarios.

### Los marcadores no aparecen

**Verificaciones**:
1. Asegúrate de que los filtros no están excluyendo todos los datos
2. Verifica que `hierarchical_k6_clustered_places.csv` contiene columnas `latitude` y `longitude`
3. Revisa que los valores no son nulos o fuera de rango

### Mapa de calor vacío

**Causa**: No hay suficientes puntos filtrados para generar el mapa de calor.
**Solución**: Amplía los filtros o selecciona más clusters.

## Despliegue en Producción

### Streamlit Cloud

1. Sube el código a GitHub
2. Conecta con Streamlit Cloud (https://streamlit.io/cloud)
3. Selecciona el repositorio y archivo `app.py`
4. Asegúrate de incluir los archivos de datos en el repositorio

### Docker

Crea un `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY ../2_Modelado/results_hierarchical_k6 ./data/

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## Contribuciones

Para mejorar la aplicación:
1. Añadir más filtros (por rango de dispositivos, estadía, etc.)
2. Implementar descarga de datos filtrados
3. Agregar gráficos estadísticos adicionales
4. Implementar búsqueda por nombre de lugar
5. Añadir comparación entre clusters

## Licencia

Este proyecto es parte del análisis de Mobilytics.
