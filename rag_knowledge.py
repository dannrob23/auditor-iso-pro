"""
Módulo RAG (Retrieval-Augmented Generation)
Este módulo convierte nuestra aplicación en un "NotebookLM" especializado.
Permite anclar el análisis del LLM a documentos oficiales (ej. PDF de la norma ISO 27001)
en lugar de depender de la memoria general del modelo.
"""
import os
import shutil
from pathlib import Path

try:
    import torchvision  # must be imported before transformers
    from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    _RAG_AVAILABLE = True
except Exception:
    _RAG_AVAILABLE = False

KB_DIR = Path("knowledge_base")
DB_DIR = Path("data/faiss_index")

KB_DIR.mkdir(exist_ok=True)
DB_DIR.parent.mkdir(exist_ok=True)

# Usamos un modelo de embeddings local y ligero (no consume créditos de API)
_embeddings_model = None

def get_embeddings():
    global _embeddings_model
    if _embeddings_model is None:
        _embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings_model

def indexar_documentos():
    """Lee todos los PDFs/TXTs en knowledge_base/, los fragmenta y los guarda en FAISS."""
    documentos = []
    
    # Verificar si hay archivos
    archivos = list(KB_DIR.glob("*.pdf")) + list(KB_DIR.glob("*.txt")) + list(KB_DIR.glob("*.docx"))
    if not archivos:
        return 0, "No se encontraron archivos en la carpeta knowledge_base/."

    for archivo in archivos:
        if archivo.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(archivo))
        elif archivo.suffix.lower() == ".txt":
            loader = TextLoader(str(archivo), encoding="utf-8")
        elif archivo.suffix.lower() == ".docx":
            loader = Docx2txtLoader(str(archivo))
        else:
            continue
        documentos.extend(loader.load())

    if not documentos:
        return 0, "Los archivos están vacíos o no se pudieron leer."

    # Dividir los documentos en fragmentos semánticos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documentos)

    # Crear la base de datos vectorial
    vectorstore = FAISS.from_documents(chunks, get_embeddings())
    
    # Guardar localmente
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)
    vectorstore.save_local(str(DB_DIR))
    
    return len(chunks), f"Se indexaron {len(chunks)} fragmentos de {len(archivos)} documentos."

def obtener_contexto(query: str, k: int = 4) -> str:
    """Busca en la norma ISO los fragmentos más relevantes para la consulta dada."""
    if not DB_DIR.exists() or not (DB_DIR / "index.faiss").exists():
        return "" # No hay base de conocimiento aún

    try:
        # Verificar que ambos archivos existan antes de intentar cargar
        faiss_file = DB_DIR / "index.faiss"
        pkl_file = DB_DIR / "index.pkl"

        if not faiss_file.exists() or not pkl_file.exists():
            # Usar st.warning si estamos en streamlit, de lo contrario no imprimir
            return ""

        # Obtener embeddings (con caché para evitar recargas)
        embeddings = get_embeddings()

        # Cargar el vectorstore
        vectorstore = FAISS.load_local(str(DB_DIR), embeddings, allow_dangerous_deserialization=True)

        # Verificar que el vectorstore tenga documentos
        if vectorstore.index is None or vectorstore.index.ntotal == 0:
            return ""

        # Realizar búsqueda
        resultados = vectorstore.similarity_search(query, k=k)

        if not resultados:
            return ""

        # Formatear el contexto recuperado
        contexto = "\n\n".join([f"--- FRAGMENTO DE LA NORMA OFICIAL ---\n{doc.page_content}" for doc in resultados])
        return contexto

    except OSError as e:
        # Error de I/O - no intentar imprimir para evitar cascada de errores
        return ""
    except Exception as e:
        # Cualquier otro error - tampoco imprimir
        return ""

def base_conocimiento_activa() -> bool:
    """Verifica si el índice FAISS existe."""
    return DB_DIR.exists() and (DB_DIR / "index.faiss").exists()
