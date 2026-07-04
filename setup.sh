#!/usr/bin/env bash
set -e

echo "🚀 Iniciando setup de Auditor ISO Pro..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Instálalo desde https://python.org"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
else
    echo "📦 Entorno virtual existente encontrado."
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env y agrega tu DEEPSEEK_API_KEY"
    echo "   Abriendo editor..."
    ${EDITOR:-nano} .env
else
    echo "⚙️ Archivo .env ya existe."
fi

# Inicializar base de datos y FAISS index
echo "🧠 Inicializando base de conocimiento RAG..."
python -c "from rag_knowledge import indexar_documentos; n, _ = indexar_documentos(); print(f'✅ Indexados {n} fragmentos')" 2>/dev/null || echo "⚠️  No se pudo indexar automáticamente. Ve a '📚 Base RAG' en la app para hacerlo manualmente."

echo ""
echo "🎉 Setup completado!"
echo "▶️  Ejecuta la aplicación con:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
