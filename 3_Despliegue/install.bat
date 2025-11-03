@echo off
echo ========================================
echo Instalacion de dependencias
echo Explorador de Clusters Jerarquicos
echo ========================================
echo.

echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Instalacion completada exitosamente!
    echo ========================================
    echo.
    echo Para ejecutar la aplicacion:
    echo   run_app.bat
    echo.
    echo O manualmente:
    echo   streamlit run app.py
    echo.
) else (
    echo.
    echo ERROR: Hubo un problema durante la instalacion.
    echo Por favor verifica tu conexion a internet y version de Python.
)

pause
