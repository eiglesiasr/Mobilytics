# Inicio Rápido - Explorador de Clusters Jerárquicos

## 🚀 Inicio en 3 Pasos

### Paso 1: Verificar datos
```bash
python check_data.py
```

Si ves "ERROR - Faltan archivos requeridos!", ejecuta primero el notebook:
- `2_Modelado/07_hierarchical_6clusters.ipynb`

### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

O usa el script de instalación:
- **Windows**: Doble click en `install.bat`
- **Linux/Mac**: `bash install.sh`

### Paso 3: Ejecutar la app
```bash
streamlit run app.py
```

O usa el script de ejecución:
- **Windows**: Doble click en `run_app.bat`
- **Linux/Mac**: `bash run_app.sh`

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 📱 Cómo usar la aplicación

### Panel Lateral (Izquierda)

1. **Selecciona el nivel de clustering:**
   - `K=3`: Macro-segmentos (3 clusters principales)
   - `K=6`: Micro-segmentos (6 clusters detallados)

2. **Elige el modo de visualización:**
   - 🔵 **Clusters**: Marcadores interactivos por cluster
   - 🔥 **Mapa de calor**: Densidad de lugares

3. **🆕 Activa el Filtro Geográfico (Recomendado para mejor rendimiento):**
   - ✅ Marca "Activar filtro por área"
   - 📍 Selecciona una ubicación:
     - Centro de San Salvador
     - Santa Tecla
     - Antiguo Cuscatlán
     - Soyapango
     - Mejicanos
     - Personalizado (ingresa tus propias coordenadas)
   - 📏 Ajusta el radio de búsqueda (0.5-20 km)
   - 💡 **Tip**: Usa 2-5 km para exploración detallada, 10-20 km para vista amplia

4. **Aplica filtros adicionales:**
   - Selecciona clusters específicos
   - Filtra por tipo de lugar (bank, residential, etc.)

5. **Explora la jerarquía:**
   - Expande los clusters K=3 para ver sus subdivisiones en K=6

### Mapa Principal (Centro)

**Modo Clusters:**
- 🖱️ **Click en marcadores** para ver información detallada
- 🔍 **Zoom y pan** para explorar diferentes áreas
- 🎨 **Colores** representan diferentes clusters

**Modo Mapa de Calor:**
- 🔥 **Zonas rojas**: Alta densidad de lugares
- 🔵 **Zonas azules**: Baja densidad de lugares
- Útil para identificar áreas con concentración de lugares

### Panel de Información (Derecha)

- 📊 **Características del cluster**: Nombre descriptivo, tamaño, métricas
- 📈 **Estadísticas detalladas**: Por cada cluster seleccionado
- 🏆 **Top 5 tipos de lugares**: Los más frecuentes en cada cluster

---

## 💡 Información en los marcadores

Al hacer click en un marcador verás:

**Identificación:**
- Nombre del lugar
- Tipo (clase)
- ID de OpenStreetMap

**Métricas Principales:**
- 👥 Dispositivos únicos: Número de visitantes diferentes
- 📊 Footfall promedio/día: Visitas diarias promedio
- 🔄 Tasa de recurrencia: % de visitantes que regresan
- ⏱️ Tiempo de estadía: Minutos promedio de permanencia

**Patrones Temporales:**
- 🕐 Hora pico (semana): Hora de mayor actividad en días laborales
- 🕐 Hora pico (fin de semana): Hora de mayor actividad en fines de semana
- ☀️ Ratio mañana/noche: Comparación de actividad diurna vs nocturna

---

## 🎯 Casos de Uso

### 1. Exploración Rápida de un Área Específica (RECOMENDADO) 🆕
1. Activa el **Filtro Geográfico**
2. Selecciona "Centro de San Salvador" y radio de 3 km
3. Selecciona `K=6` para ver detalles
4. Haz click en marcadores para ver información específica
5. **Resultado**: Vista rápida y eficiente de ~500-1000 lugares

### 2. Análisis General
1. Selecciona `K=3` para ver macro-segmentos
2. Usa **Mapa de calor** para identificar zonas de interés
3. Cambia a **Clusters** para ver lugares individuales

### 3. Análisis Detallado
1. Selecciona `K=6` para micro-segmentos
2. Filtra por cluster de interés
3. Explora marcadores individuales para información específica

### 4. Comparación de Clusters
1. Selecciona múltiples clusters en el filtro
2. Observa diferencias de color en el mapa
3. Compara estadísticas en el panel derecho

### 5. Búsqueda por Tipo de Lugar
1. Filtra por tipo específico (ej: "bank")
2. Observa su distribución geográfica
3. Identifica patrones de clustering

### 6. Análisis Jerárquico
1. Usa el árbol jerárquico en el sidebar
2. Identifica cómo se subdividen los clusters K=3 en K=6
3. Compara características entre niveles

---

## 📊 Interpretación de Métricas

### Dispositivos Únicos
- **Alto (>100)**: Lugares muy visitados, alta visibilidad
- **Medio (30-100)**: Tráfico moderado
- **Bajo (<30)**: Tráfico específico o limitado

### Tasa de Recurrencia
- **Alta (>40%)**: Lugares de uso frecuente (oficinas, hogares)
- **Media (20-40%)**: Uso regular
- **Baja (<20%)**: Lugares de paso o visita única

### Tiempo de Estadía
- **Largo (>300 min)**: Lugares de permanencia (residencias, trabajo)
- **Medio (60-300 min)**: Visitas extendidas (tiendas, restaurantes)
- **Corto (<60 min)**: Visitas breves (bancos, servicios)

---

## 🔧 Solución de Problemas Comunes

### El mapa no carga
- Verifica tu conexión a internet
- Espera unos segundos, puede estar cargando datos
- Recarga la página (F5)

### No veo marcadores
- Verifica que los filtros no excluyen todo
- Selecciona más clusters en el filtro
- Cambia de modo "Mapa de calor" a "Clusters"

### Error al cargar datos
- Ejecuta `python check_data.py` para verificar archivos
- Ejecuta el notebook `07_hierarchical_6clusters.ipynb`
- Verifica que existe la carpeta `results_hierarchical_k6`

### La aplicación es lenta
- **Activa el Filtro Geográfico** (la solución más efectiva) 🆕
- Reduce el radio de búsqueda a 2-5 km
- Usa "Mapa de calor" en lugar de "Clusters" para muchos puntos
- Reduce el número de clusters seleccionados
- Cierra otros programas para liberar memoria

---

## 📖 Más Información

Para documentación completa, consulta [README.md](README.md)

Para reportar problemas o sugerencias, contacta al equipo de Mobilytics.

---

**¡Disfruta explorando los clusters jerárquicos!** 🎉
