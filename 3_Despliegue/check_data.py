"""
Script to verify that all required data files exist before running the Streamlit app.
"""
import sys
from pathlib import Path

def check_data_files():
    """Check if all required data files exist"""

    base_path = Path(__file__).parent.parent / "2_Modelado" / "results_hierarchical_k6"

    required_files = [
        "hierarchical_k6_clustered_places.csv",
        "hierarchical_structure_k3_k6.csv",
        "cluster_characteristics.json",
        "hierarchical_k6_cluster_statistics.csv"
    ]

    print("Verificando archivos de datos requeridos...")
    print(f"Ruta base: {base_path}")
    print("-" * 70)

    all_exist = True

    for filename in required_files:
        filepath = base_path / filename
        exists = filepath.exists()

        if exists:
            size = filepath.stat().st_size / 1024  # KB
            status = f"OK - Encontrado ({size:.1f} KB)"
        else:
            status = "ERROR - NO ENCONTRADO"
            all_exist = False

        print(f"{filename:<40} {status}")

    print("-" * 70)

    if all_exist:
        print("OK - Todos los archivos requeridos existen!")
        print("\nPuedes ejecutar la aplicacion con:")
        print("  streamlit run app.py")
        return 0
    else:
        print("ERROR - Faltan archivos requeridos!")
        print("\nPara generar los datos:")
        print("  1. Abre el notebook: 2_Modelado/07_hierarchical_6clusters.ipynb")
        print("  2. Ejecuta todas las celdas (Run All)")
        print("  3. Verifica que se creo la carpeta results_hierarchical_k6")
        return 1

if __name__ == "__main__":
    exit_code = check_data_files()
    sys.exit(exit_code)
