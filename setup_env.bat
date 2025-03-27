@echo off
SETLOCAL ENABLEEXTENSIONS

SET VENV_DIR=venv

REM Crear entorno virtual si no existe
IF NOT EXIST %VENV_DIR% (
    echo [INFO] Creando entorno virtual...
    python -m venv %VENV_DIR%
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
CALL %VENV_DIR%\Scripts\activate.bat

REM Actualizar pip
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip

REM Instalar pygame-ce
echo [INFO] Instalando pygame-ce...
pip install pygame-ce --upgrade

REM Desinstalar pygame clásico si existe
echo [INFO] Eliminando pygame clásico (si existe)...
pip uninstall pygame -y >nul 2>&1

REM Instalar pyinstaller
echo [INFO] Instalando pyinstaller...
pip install pyinstaller --upgrade

REM Instalar pygbag
echo [INFO] Instalando pygbag...
pip install pygbag --upgrade

REM Instalar esper versión 2.5
echo [INFO] Instalando esper==2.5...
pip install esper==2.5

REM Mostrar versiones instaladas
echo.
echo ================================
echo ✅ VERIFICACIÓN DE INSTALACIÓN
echo ================================
pip show pygame-ce | findstr Version
pip show pyinstaller | findstr Version
pip show pygbag | findstr Version
pip show esper | findstr Version
echo ================================

echo.
echo 🟢 Todo listo. El entorno está preparado.
PAUSE
ENDLOCAL
