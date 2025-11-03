#!/bin/bash
echo "========================================"
echo "Explorador de Clusters Jerarquicos"
echo "========================================"
echo ""

echo "Verificando archivos de datos..."
python check_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Iniciando aplicacion Streamlit..."
    streamlit run app.py
else
    echo ""
    echo "ERROR: No se pueden cargar los datos."
    echo "Por favor ejecuta el notebook 07_hierarchical_6clusters.ipynb primero."
fi
