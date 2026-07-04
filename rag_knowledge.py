"""
Módulo RAG (Retrieval-Augmented Generation)
Este módulo convierte nuestra aplicación en un "NotebookLM" especializado.
Permite anclar el análisis del LLM a documentos oficiales (ej. PDF de la norma ISO 27001)
en lugar de depender de la memoria general del modelo.
"""
import os
import shutil
from pathlib import Path

# Todos los imports de RAG son opcionales para no romper la app si faltan dependencias
_RAG_AVAILABLE = False
_HAS_PDF = False
_HAS_TXT = False
_HAS_DOCX = False

try:
    from langchain_community.document_loaders import PyPDFLoader
    _HAS_PDF = True
except Exception:
    pass

try:
    from langchain_community.document_loaders import TextLoader
    _HAS_TXT = True
except Exception:
    pass

try:
    from langchain_community.document_loaders import Docx2txtLoader
    _HAS_DOCX = True
except Exception:
    pass

try:
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

_embeddings_model = None

def get_embeddings():
    global _embeddings_model
    if _embeddings_model is None:
        if not _RAG_AVAILABLE:
            raise RuntimeError("Dependencias de RAG no disponibles")
        _embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings_model

def indexar_documentos():
    """Lee los documentos soportados en knowledge_base/, los fragmenta y los guarda en FAISS."""
    if not _RAG_AVAILABLE:
        return 0, "RAG no disponible: faltan dependencias base."

    archivos = []
    if _HAS_PDF:
        archivos.extend(KB_DIR.glob("*.pdf"))
    if _HAS_TXT:
        archivos.extend(KB_DIR.glob("*.txt"))
    if _HAS_DOCX:
        archivos.extend(KB_DIR.glob("*.docx"))

    if not archivos:
        return 0, "No se encontraron archivos indexables en knowledge_base/."

    documentos = []
    errores = []

    for archivo in archivos:
        suffix = archivo.suffix.lower()
        try:
            if suffix == ".pdf" and _HAS_PDF:
                documentos.extend(PyPDFLoader(str(archivo)).load())
            elif suffix == ".txt" and _HAS_TXT:
                documentos.extend(TextLoader(str(archivo), encoding="utf-8").load())
            elif suffix == ".docx" and _HAS_DOCX:
                documentos.extend(Docx2txtLoader(str(archivo)).load())
        except Exception as e:
            errores.append(f"{archivo.name}: {e}")

    if not documentos:
        return 0, "No se pudo extraer texto de los documentos. Detalles: " + "; ".join(errores)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documentos)

    vectorstore = FAISS.from_documents(chunks, get_embeddings())
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)
    vectorstore.save_local(str(DB_DIR))

    msg = f"Se indexaron {len(chunks)} fragmentos de {len(archivos)} documentos."
    if errores:
        msg += f" Algunos archivos no se pudieron leer: " + "; ".join(errores)
    return len(chunks), msg

def obtener_contexto(query: str, k: int = 4) -> str:
    """Busca en la norma ISO los fragmentos más relevantes para la consulta dada."""
    if not DB_DIR.exists() or not (DB_DIR / "index.faiss").exists():
        return ""

    try:
        faiss_file = DB_DIR / "index.faiss"
        pkl_file = DB_DIR / "index.pkl"
        if not faiss_file.exists() or not pkl_file.exists():
            return ""

        embeddings = get_embeddings()
        vectorstore = FAISS.load_local(str(DB_DIR), embeddings, allow_dangerous_deserialization=True)

        if vectorstore.index is None or vectorstore.index.ntotal == 0:
            return ""

        resultados = vectorstore.similarity_search(query, k=k)
        if not resultados:
            return ""

        return "\n\n".join([f"--- FRAGMENTO DE LA NORMA OFICIAL ---\n{doc.page_content}" for doc in resultados])
    except OSError:
        return ""
    except Exception:
        return ""

def base_conocimiento_activa() -> bool:
    """Verifica si el índice FAISS existe."""
    return DB_DIR.exists() and (DB_DIR / "index.faiss").exists()
