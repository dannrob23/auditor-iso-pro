@echo off
chcp 65001 >nul
echo 🚀 Iniciando setup de Auditor ISO Pro...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Instálalo desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Crear entorno virtual si no existe
if not exist "venv\" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
) else (
    echo 📦 Entorno virtual existente encontrado.
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo ⬆️ Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📥 Instalando dependencias...
pip install -r requirements.txt

REM Crear .env si no existe
if not exist ".env" (
    echo ⚙️ Creando archivo .env desde .env.example...
    copy .env.example .env
    echo ⚠️  IMPORTANTE: Edita el archivo .env y agrega tu DEEPSEEK_API_KEY
    notepad .env
) else (
    echo ⚙️ Archivo .env ya existe.
)

echo.
echo 🎉 Setup completado!
echo ▶️  Ejecuta la aplicación con:
echo    venv\Scripts\activate.bat
echo    streamlit run app.py
pause
