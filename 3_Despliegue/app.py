import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import json
import numpy as np
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

# Page configuration
st.set_page_config(
    page_title="Hierarchical Cluster Explorer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .cluster-info {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def filter_by_radius(df, center_lat, center_lon, radius_km):
    """Filter dataframe to only include points within radius_km of center point"""
    if radius_km is None or radius_km <= 0:
        return df

    # Calculate distance for each point
    df['distance_km'] = df.apply(
        lambda row: haversine_distance(center_lat, center_lon, row['latitude'], row['longitude']),
        axis=1
    )

    # Filter by radius
    filtered_df = df[df['distance_km'] <= radius_km].copy()

    return filtered_df

@st.cache_data
def load_data():
    """Load clustering results and hierarchy data"""
    # Load k=6 hierarchical clustering results
    data_path = Path(__file__).parent.parent / "2_Modelado" / "results_hierarchical_k6"

    # Load main clustering data
    df = pd.read_csv(data_path / "hierarchical_k6_clustered_places.csv")

    # Load hierarchy structure
    hierarchy_df = pd.read_csv(data_path / "hierarchical_structure_k3_k6.csv")

    # Load cluster characteristics
    with open(data_path / "cluster_characteristics.json", 'r', encoding='utf-8') as f:
        characteristics = json.load(f)

    return df, hierarchy_df, characteristics

@st.cache_data
def load_cluster_profiles():
    """Load cluster profiling data"""
    data_path = Path(__file__).parent.parent / "2_Modelado" / "results_hierarchical_k6"
    profile_df = pd.read_csv(data_path / "hierarchical_k6_cluster_statistics.csv")
    return profile_df

def get_cluster_color(cluster_id, level='k6'):
    """Get color for cluster visualization"""
    if level == 'k3':
        colors = ['#e74c3c', '#3498db', '#2ecc71']
        return colors[cluster_id % len(colors)]
    else:  # k6
        colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6']
        return colors[cluster_id % len(colors)]

def create_base_map(center_lat=13.6929, center_lon=-89.2182, zoom=12):
    """Create base folium map centered on San Salvador, El Salvador"""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    return m

def create_cluster_map(df_filtered, cluster_level='k6', show_heatmap=False,
                       geo_center=None, geo_radius=None):
    """Create interactive cluster map

    Args:
        df_filtered: Filtered dataframe
        cluster_level: 'k3' or 'k6'
        show_heatmap: If True, show heatmap instead of markers
        geo_center: Tuple (lat, lon) for geographic filter center
        geo_radius: Radius in km for geographic filter visualization
    """
    # Calculate center
    center_lat = df_filtered['latitude'].mean()
    center_lon = df_filtered['longitude'].mean()

    m = create_base_map(center_lat, center_lon)

    # Add geographic filter visualization if active
    if geo_center is not None and geo_radius is not None:
        # Add circle showing search radius
        folium.Circle(
            location=geo_center,
            radius=geo_radius * 1000,  # Convert km to meters
            color='#3498db',
            fill=True,
            fillColor='#3498db',
            fillOpacity=0.1,
            weight=2,
            popup=f"Radio de búsqueda: {geo_radius} km"
        ).add_to(m)

        # Add marker at center
        folium.Marker(
            location=geo_center,
            popup=f"Centro de búsqueda<br>{geo_center[0]:.4f}, {geo_center[1]:.4f}",
            icon=folium.Icon(color='blue', icon='crosshairs', prefix='fa')
        ).add_to(m)

    if show_heatmap:
        # Create heatmap
        heat_data = [[row['latitude'], row['longitude']]
                     for idx, row in df_filtered.iterrows()]
        plugins.HeatMap(heat_data, radius=15, blur=25, max_zoom=13).add_to(m)
    else:
        # Create marker cluster
        marker_cluster = plugins.MarkerCluster().add_to(m)

        # Determine cluster column
        cluster_col = 'cluster_k3' if cluster_level == 'k3' else 'cluster'

        # Add markers
        for idx, row in df_filtered.iterrows():
            cluster_id = row[cluster_col]
            color = get_cluster_color(cluster_id, cluster_level)

            # Create popup content
            nombre = row.get('nombre', 'Unknown Place')
            if pd.isna(nombre) or nombre == '':
                nombre = f"{row.get('clase', 'Place').title()}"

            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 280px;">
                <h4 style="margin: 0 0 10px 0; color: {color};">
                    {nombre}
                </h4>
                <hr style="margin: 5px 0;">
                <b>Cluster:</b> {cluster_level.upper()} - {cluster_id}<br>
                <b>Tipo:</b> {row.get('clase', 'N/A')}<br>
                <b>OSM ID:</b> {row.get('osm_id', 'N/A')}<br>
                <hr style="margin: 5px 0;">
                <b>📊 Métricas Principales:</b><br>
                <b>• Dispositivos únicos:</b> {int(row.get('unique_devices_count', 0)):,}<br>
                <b>• Footfall promedio/día:</b> {row.get('footfall_avg_per_day', 0):.1f}<br>
                <b>• Tasa de recurrencia:</b> {row.get('recurrence_rate', 0):.2%}<br>
                <b>• Tiempo de estadía (min):</b> {row.get('dwell_time_mean', 0):.1f}<br>
                <hr style="margin: 5px 0;">
                <b>⏰ Patrones Temporales:</b><br>
                <b>• Hora pico (semana):</b> {format_peak_hour(row.get('peak_hour_weekday', ''))}<br>
                <b>• Hora pico (fin de semana):</b> {format_peak_hour(row.get('peak_hour_weekend', ''))}<br>
                <b>• Ratio mañana/noche:</b> {row.get('morning_to_evening_ratio', 0):.2f}<br>
            </div>
            """

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(marker_cluster)

    return m

def format_peak_hour(peak_hour_value):
    """Format peak hour value"""
    if pd.isna(peak_hour_value) or peak_hour_value == '':
        return "N/A"

    try:
        hour = int(float(peak_hour_value))
        return f"{hour:02d}:00"
    except:
        return "N/A"

def display_cluster_characteristics(characteristics, cluster_id, level='k6'):
    """Display cluster characteristics in sidebar"""
    cluster_key = f"{level}_clusters"

    if cluster_key in characteristics and str(cluster_id) in characteristics[cluster_key]:
        char = characteristics[cluster_key][str(cluster_id)]

        st.markdown(f"""
        <div class="cluster-info">
            <h3 style="margin-top: 0; color: {get_cluster_color(cluster_id, level)};">
                {level.upper()} Cluster {cluster_id}
            </h3>
            <p><b>Nombre:</b> {char.get('descriptive_name', 'N/A')}</p>
            <p><b>Tamaño:</b> {char.get('size', 0):,} lugares ({char.get('pct_of_total', 0):.1f}%)</p>
            <p><b>Tipo dominante:</b> {char.get('dominant_type', 'N/A').title()}</p>
            <p><b>Nivel de actividad:</b> {char.get('activity_level', 'N/A')}</p>
            <p><b>Patrón de visita:</b> {char.get('visit_pattern', 'N/A')}</p>
            <p><b>Categoría de estadía:</b> {char.get('dwell_category', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Visitantes promedio", f"{char.get('avg_visitors', 0):.0f}")
        with col2:
            st.metric("Estadía (min)", f"{char.get('avg_dwell_time', 0):.0f}")

def display_hierarchy_tree(characteristics, hierarchy_map):
    """Display hierarchical structure"""
    st.markdown("### 🌳 Estructura Jerárquica")

    k3_clusters = characteristics.get('k3_clusters', {})
    k6_clusters = characteristics.get('k6_clusters', {})

    for k3_id in range(3):
        k3_char = k3_clusters.get(str(k3_id), {})

        with st.expander(f"📁 K=3 Cluster {k3_id}: {k3_char.get('descriptive_name', 'N/A')}"):
            st.write(f"**Tamaño:** {k3_char.get('size', 0):,} lugares")
            st.write(f"**Porcentaje:** {k3_char.get('pct_of_total', 0):.1f}%")

            # Find children
            children = hierarchy_map.get(str(k3_id), {}).get('k6_children', [])

            st.markdown("**Subdivisiones en K=6:**")
            for k6_id in children:
                k6_char = k6_clusters.get(str(k6_id), {})
                st.markdown(f"""
                - **Cluster {k6_id}:** {k6_char.get('descriptive_name', 'N/A')}
                  *{k6_char.get('size', 0):,} lugares ({k6_char.get('pct_of_total', 0):.1f}%)*
                """)

def main():
    # Header
    st.title("🗺️ Explorador de Clusters Jerárquicos")
    st.markdown("**Análisis espacial y comportamental de lugares - San Salvador, El Salvador**")

    # Load data
    try:
        df, hierarchy_df, characteristics = load_data()
        cluster_profiles = load_cluster_profiles()
        hierarchy_map = characteristics.get('hierarchy_map', {})
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        st.info("Asegúrate de ejecutar el notebook 07_hierarchical_6clusters.ipynb primero para generar los datos.")
        return

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")

        # Cluster level selection
        cluster_level = st.radio(
            "Nivel de clustering:",
            options=['k3', 'k6'],
            format_func=lambda x: f"K=3 (Macro-segmentos)" if x == 'k3' else f"K=6 (Micro-segmentos)",
            index=1
        )

        # Visualization mode
        viz_mode = st.radio(
            "Modo de visualización:",
            options=['clusters', 'heatmap'],
            format_func=lambda x: "🔵 Clusters (marcadores)" if x == 'clusters' else "🔥 Mapa de calor"
        )

        st.markdown("---")

        # Geographic filter
        st.subheader("🌍 Filtro Geográfico")

        use_geo_filter = st.checkbox("Activar filtro por área", value=False,
                                      help="Filtra lugares dentro de un radio específico para mejorar rendimiento")

        if use_geo_filter:
            # Preset locations
            presets = {
                "Centro de San Salvador": (13.6929, -89.2182),
                "Santa Tecla": (13.6769, -89.2797),
                "Antiguo Cuscatlán": (13.6647, -89.2539),
                "Soyapango": (13.7102, -89.1397),
                "Mejicanos": (13.7250, -89.2119),
                "Personalizado": None
            }

            selected_preset = st.selectbox(
                "Ubicación:",
                options=list(presets.keys()),
                help="Selecciona una ubicación predefinida o usa coordenadas personalizadas"
            )

            if selected_preset == "Personalizado":
                col1, col2 = st.columns(2)
                with col1:
                    center_lat = st.number_input(
                        "Latitud:",
                        value=13.6929,
                        format="%.6f",
                        help="Latitud del centro del área"
                    )
                with col2:
                    center_lon = st.number_input(
                        "Longitud:",
                        value=-89.2182,
                        format="%.6f",
                        help="Longitud del centro del área"
                    )
            else:
                center_lat, center_lon = presets[selected_preset]
                st.info(f"📍 {selected_preset}: {center_lat:.4f}, {center_lon:.4f}")

            # Radius selection
            radius_km = st.slider(
                "Radio (km):",
                min_value=0.5,
                max_value=20.0,
                value=5.0,
                step=0.5,
                help="Radio de búsqueda desde el punto central"
            )

            # Apply geographic filter
            df = filter_by_radius(df, center_lat, center_lon, radius_km)

            # Show filter stats
            st.success(f"✓ {len(df):,} lugares encontrados en {radius_km} km")

            # Store for map visualization
            geo_filter_center = (center_lat, center_lon)
            geo_filter_radius = radius_km
        else:
            st.info(f"📊 Total: {len(df):,} lugares")
            geo_filter_center = None
            geo_filter_radius = None

        st.markdown("---")

        # Cluster filter
        if cluster_level == 'k3':
            available_clusters = sorted(df['cluster_k3'].unique())
            cluster_filter = st.multiselect(
                "Filtrar por K=3 Clusters:",
                options=available_clusters,
                default=available_clusters
            )
        else:
            available_clusters = sorted(df['cluster'].unique())
            cluster_filter = st.multiselect(
                "Filtrar por K=6 Clusters:",
                options=available_clusters,
                default=available_clusters
            )

        st.markdown("---")

        # Place type filter
        place_types = sorted(df['clase'].unique())
        type_filter = st.multiselect(
            "Filtrar por tipo de lugar:",
            options=place_types,
            default=place_types
        )

        st.markdown("---")

        # Display hierarchy tree
        display_hierarchy_tree(characteristics, hierarchy_map)

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Mapa Interactivo")

        # Filter data
        if cluster_level == 'k3':
            df_filtered = df[
                (df['cluster_k3'].isin(cluster_filter)) &
                (df['clase'].isin(type_filter))
            ]
        else:
            df_filtered = df[
                (df['cluster'].isin(cluster_filter)) &
                (df['clase'].isin(type_filter))
            ]

        # Display metrics
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("Total lugares", f"{len(df_filtered):,}")
        with metric_cols[1]:
            st.metric("Clusters visibles", len(cluster_filter))
        with metric_cols[2]:
            avg_devices = df_filtered['unique_devices_count'].mean()
            st.metric("Dispositivos promedio", f"{avg_devices:.0f}")
        with metric_cols[3]:
            avg_dwell = df_filtered['dwell_time_mean'].mean()
            st.metric("Estadía promedio (min)", f"{avg_dwell:.0f}")

        # Create and display map
        show_heatmap = (viz_mode == 'heatmap')

        # Warning if too many markers
        MAX_MARKERS = 5000
        if not show_heatmap and len(df_filtered) > MAX_MARKERS:
            st.warning(f"⚠️ Hay {len(df_filtered):,} lugares a renderizar. "
                      f"Considera usar el filtro geográfico o el mapa de calor para mejor rendimiento. "
                      f"Mostrando los primeros {MAX_MARKERS:,} lugares.")
            df_to_map = df_filtered.head(MAX_MARKERS)
        else:
            df_to_map = df_filtered

        m = create_cluster_map(df_to_map, cluster_level, show_heatmap,
                              geo_center=geo_filter_center, geo_radius=geo_filter_radius)

        # Display map
        st_data = st_folium(m, width=None, height=600)

        # Info about interaction
        if viz_mode == 'clusters':
            if len(df_filtered) <= MAX_MARKERS:
                st.info("💡 Haz click en los marcadores para ver información detallada de cada lugar")
            else:
                st.info(f"💡 Mostrando {MAX_MARKERS:,} de {len(df_filtered):,} lugares. "
                       f"Usa el filtro geográfico para explorar áreas específicas.")

    with col2:
        st.subheader("Información de Clusters")

        # Display characteristics for selected clusters
        for cluster_id in cluster_filter:
            display_cluster_characteristics(characteristics, cluster_id, cluster_level)

        st.markdown("---")

        # Cluster statistics
        st.subheader("📊 Estadísticas")

        for cluster_id in cluster_filter:
            if cluster_level == 'k3':
                cluster_data = df_filtered[df_filtered['cluster_k3'] == cluster_id]
            else:
                cluster_data = df_filtered[df_filtered['cluster'] == cluster_id]

            if len(cluster_data) > 0:
                with st.expander(f"Cluster {cluster_id} - Estadísticas detalladas"):
                    st.write(f"**Lugares:** {len(cluster_data):,}")
                    st.write(f"**Dispositivos únicos (promedio):** {cluster_data['unique_devices_count'].mean():.0f}")
                    st.write(f"**Footfall/día (promedio):** {cluster_data['footfall_avg_per_day'].mean():.1f}")
                    st.write(f"**Recurrencia (promedio):** {cluster_data['recurrence_rate'].mean():.2%}")
                    st.write(f"**Tiempo de estadía (promedio):** {cluster_data['dwell_time_mean'].mean():.1f} min")

                    # Top place types
                    st.markdown("**Top 5 tipos de lugares:**")
                    top_types = cluster_data['clase'].value_counts().head(5)
                    for place_type, count in top_types.items():
                        pct = 100 * count / len(cluster_data)
                        st.write(f"- {place_type}: {count} ({pct:.1f}%)")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>Explorador de Clusters Jerárquicos | Análisis de Movilidad Urbana</p>
        <p>Datos: San Salvador, El Salvador | Clustering: Jerarquico Aglomerativo (Ward)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
