import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from pathlib import Path
from shapely import wkt
from math import radians, cos, sin, asin, sqrt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="KMeans Cluster Explorer",
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
    """Calculate distance between two points in km"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return c * 6371  # Earth radius in km

@st.cache_data
def load_data():
    """Load KMeans clustering results"""
    data_path = Path(__file__).parent.parent / "2_Modelado" / "results"
    df = pd.read_csv(data_path / "kmeans_clustered_places.csv")

    # Extract coordinates if needed
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        def extract_coords(geom_wkt):
            try:
                geom = wkt.loads(geom_wkt)
                centroid = geom.centroid
                return pd.Series({'latitude': centroid.y, 'longitude': centroid.x})
            except:
                return pd.Series({'latitude': None, 'longitude': None})

        df[['latitude', 'longitude']] = df['geometry_wkt'].apply(extract_coords)

    df = df.dropna(subset=['latitude', 'longitude'])
    return df

def get_cluster_objective(cluster_id):
    """Get objective for each cluster"""
    objectives = {
        0: "Incrementar visitas y frecuencia",
        1: "Fidelizar visitas ocasionales",
        2: "Maximizar valor por visita y presencia de marca",
        3: "Profundizar relación y aprovechar recurrencia"
    }
    return objectives.get(int(cluster_id), "N/A")

def get_cluster_color(cluster_id):
    """Get color for cluster"""
    colors = {0: 'red', 1: 'orange', 2: 'green', 3: 'blue'}
    return colors.get(int(cluster_id), 'gray')

def create_map(df_filtered, center_lat, center_lon, geo_center=None, geo_radius=None):
    """Create folium map with markers"""
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='OpenStreetMap')

    # Add geographic filter circle if active
    if geo_center is not None and geo_radius is not None:
        folium.Circle(
            location=[geo_center[0], geo_center[1]],
            radius=geo_radius * 1000,
            color='#3498db',
            fill=True,
            fillColor='#3498db',
            fillOpacity=0.1,
            weight=2
        ).add_to(m)

        folium.Marker(
            location=[geo_center[0], geo_center[1]],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Add markers
    for _, row in df_filtered.iterrows():
        cluster_id = int(row['cluster'])
        color = get_cluster_color(cluster_id)

        # Get place name
        nombre = str(row.get('nombre', ''))
        if pd.isna(row.get('nombre')) or nombre == '' or nombre == 'nan':
            nombre = str(row.get('clase', 'Place')).title()

        # Create simple popup
        popup_text = f"""
        <b>{nombre}</b><br>
        Cluster: {cluster_id}<br>
        Objetivo: {get_cluster_objective(cluster_id)}<br>
        Visitantes: {int(row.get('unique_devices_count', 0)):,}<br>
        """

        folium.Marker(
            location=[float(row['latitude']), float(row['longitude'])],
            popup=popup_text,
            tooltip=f"Cluster {cluster_id}: {nombre}",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

    return m

def main():
    st.title("🗺️ Explorador de Clusters KMeans")
    st.markdown("**Análisis espacial y comportamental de lugares - San Salvador, El Salvador**")

    # Load data
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")

        # Geographic filter
        st.subheader("🌍 Filtro Geográfico")
        use_geo_filter = st.checkbox("Activar filtro por área", value=False)

        if use_geo_filter:
            presets = {
                "Centro de San Salvador": (13.6929, -89.2182),
                "Santa Tecla": (13.6769, -89.2797),
                "Antiguo Cuscatlán": (13.6647, -89.2539)
            }

            selected_preset = st.selectbox("Ubicación:", list(presets.keys()))
            center_lat, center_lon = presets[selected_preset]
            radius_km = st.slider("Radio (km):", 0.5, 20.0, 5.0, 0.5)

            # Filter by radius
            df['distance_km'] = df.apply(
                lambda row: haversine_distance(center_lat, center_lon,
                                              row['latitude'], row['longitude']),
                axis=1
            )
            df = df[df['distance_km'] <= radius_km].copy()

            st.success(f"✓ {len(df):,} lugares encontrados")
            geo_filter_center = (center_lat, center_lon)
            geo_filter_radius = radius_km
        else:
            st.info(f"📊 Total: {len(df):,} lugares")
            geo_filter_center = None
            geo_filter_radius = None

        st.markdown("---")

        # Cluster filter
        st.subheader("🎯 Filtrar por Clusters")
        all_clusters = sorted(df['cluster'].unique())
        selected_clusters = st.multiselect(
            "Selecciona clusters:",
            options=all_clusters,
            default=all_clusters,
            format_func=lambda x: f"Cluster {x}: {get_cluster_objective(x)}"
        )

        st.markdown("---")

        # Summary
        st.subheader("📊 Resumen")
        for cluster_id in all_clusters:
            cluster_data = df[df['cluster'] == cluster_id]
            pct = 100 * len(cluster_data) / len(df)

            with st.expander(f"Cluster {cluster_id} ({len(cluster_data):,})"):
                st.write(f"**Objetivo:** {get_cluster_objective(cluster_id)}")
                st.write(f"**Porcentaje:** {pct:.1f}%")
                st.write(f"**Visitantes promedio:** {cluster_data['unique_devices_count'].mean():.0f}")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Mapa Interactivo")

        # Filter data
        df_filtered = df[df['cluster'].isin(selected_clusters)]

        # Metrics
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("Total lugares", f"{len(df_filtered):,}")
        with metric_cols[1]:
            st.metric("Clusters", len(selected_clusters))
        with metric_cols[2]:
            st.metric("Visitantes promedio", f"{df_filtered['unique_devices_count'].mean():.0f}")
        with metric_cols[3]:
            st.metric("Estadía promedio", f"{df_filtered['dwell_time_mean'].mean():.0f} min")

        # Limit markers for performance
        MAX_MARKERS = 1000
        if len(df_filtered) > MAX_MARKERS:
            st.warning(f"⚠️ Mostrando {MAX_MARKERS:,} de {len(df_filtered):,} lugares")
            df_to_map = df_filtered.head(MAX_MARKERS)
        else:
            df_to_map = df_filtered

        # Create map
        center_lat = df_to_map['latitude'].mean()
        center_lon = df_to_map['longitude'].mean()

        m = create_map(df_to_map, center_lat, center_lon, geo_filter_center, geo_filter_radius)

        # Display map using folium_static instead of st_folium
        folium_static(m, width=800, height=600)

    with col2:
        st.subheader("Información de Clusters")

        for cluster_id in selected_clusters:
            cluster_data = df_filtered[df_filtered['cluster'] == cluster_id]

            if len(cluster_data) > 0:
                st.markdown(f"""
                <div class="cluster-info">
                    <h3 style="color: {get_cluster_color(cluster_id)};">Cluster {cluster_id}</h3>
                    <p><b>🎯 Objetivo:</b> {get_cluster_objective(cluster_id)}</p>
                    <p><b>Lugares:</b> {len(cluster_data):,}</p>
                </div>
                """, unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Visitantes", f"{cluster_data['unique_devices_count'].mean():.0f}")
                with col_b:
                    st.metric("Estadía (min)", f"{cluster_data['dwell_time_mean'].mean():.0f}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <p>Explorador de Clusters KMeans | Análisis de Movilidad Urbana</p>
        <p>Datos: San Salvador, El Salvador | Clustering: KMeans (K=4)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
