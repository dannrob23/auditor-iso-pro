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
UPLOADS_DIR = Path("uploads")
DB_DIR = Path("data/faiss_index")
DB_UPLOADS_DIR = Path("data/faiss_index_uploads")

KB_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
DB_DIR.parent.mkdir(exist_ok=True)
DB_UPLOADS_DIR.parent.mkdir(exist_ok=True)

_embeddings_model = None

def get_embeddings():
    global _embeddings_model
    if _embeddings_model is None:
        if not _RAG_AVAILABLE:
            raise RuntimeError("Dependencias de RAG no disponibles")
        _embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings_model

def _archivos_indexables(directorio: Path):
    archivos = []
    if _HAS_PDF:
        archivos.extend(directorio.glob("*.pdf"))
    if _HAS_TXT:
        archivos.extend(directorio.glob("*.txt"))
    if _HAS_DOCX:
        archivos.extend(directorio.glob("*.docx"))
    return archivos

def _cargar_documento(archivo: Path):
    suffix = archivo.suffix.lower()
    if suffix == ".pdf" and _HAS_PDF:
        return PyPDFLoader(str(archivo)).load()
    elif suffix == ".txt" and _HAS_TXT:
        return TextLoader(str(archivo), encoding="utf-8").load()
    elif suffix == ".docx" and _HAS_DOCX:
        return Docx2txtLoader(str(archivo)).load()
    return []

def _crear_indice(documentos, destino: Path):
    if not documentos:
        return 0
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documentos)
    if not chunks:
        return 0
    try:
        embeddings = get_embeddings()
        if embeddings is None:
            return 0
        textos = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        vectorstore = FAISS.from_texts(textos, embeddings, metadatas=metadatas)
    except Exception:
        return 0
    if destino.exists():
        shutil.rmtree(destino)
    vectorstore.save_local(str(destino))
    return len(chunks)

def indexar_documentos():
    """Indexa solo la base oficial de knowledge_base/."""
    if not _RAG_AVAILABLE:
        return 0, "RAG no disponible: faltan dependencias base."

    archivos = _archivos_indexables(KB_DIR)
    if not archivos:
        return 0, "No se encontraron archivos indexables en knowledge_base/."

    documentos = []
    errores = []
    for archivo in archivos:
        try:
            documentos.extend(_cargar_documento(archivo))
        except Exception as e:
            errores.append(f"{archivo.name}: {e}")

    if not documentos:
        return 0, "No se pudo extraer texto de los documentos oficiales. Detalles: " + "; ".join(errores)

    num_chunks = _crear_indice(documentos, DB_DIR)
    msg = f"Base oficial: se indexaron {num_chunks} fragmentos de {len(archivos)} documentos."
    if errores:
        msg += f" Algunos archivos no se pudieron leer: " + "; ".join(errores)
    return num_chunks, msg

def indexar_documentos_temporales():
    """Indexa solo los archivos de la carpeta temporal uploads/."""
    if not _RAG_AVAILABLE:
        return 0, "RAG no disponible: faltan dependencias base."

    archivos = _archivos_indexables(UPLOADS_DIR)
    if not archivos:
        return 0, "No se encontraron archivos temporales en uploads/."

    documentos = []
    errores = []
    for archivo in archivos:
        try:
            documentos.extend(_cargar_documento(archivo))
        except Exception as e:
            errores.append(f"{archivo.name}: {e}")

    if not documentos:
        return 0, "No se pudo extraer texto de los documentos temporales. Detalles: " + "; ".join(errores)

    num_chunks = _crear_indice(documentos, DB_UPLOADS_DIR)
    msg = f"Uploads: se indexaron {num_chunks} fragmentos de {len(archivos)} documentos."
    if errores:
        msg += f" Algunos archivos no se pudieron leer: " + "; ".join(errores)
    return num_chunks, msg

def listar_uploads():
    return sorted(UPLOADS_DIR.glob("*")) if UPLOADS_DIR.exists() else []

def limpiar_uploads():
    if UPLOADS_DIR.exists():
        for archivo in UPLOADS_DIR.glob("*"):
            if archivo.is_file():
                archivo.unlink()
    if DB_UPLOADS_DIR.exists():
        shutil.rmtree(DB_UPLOADS_DIR)
    return True

def obtener_contexto(query: str, k: int = 4, incluir_uploads: bool = True) -> str:
    """Busca en la norma oficial y, opcionalmente, en uploads temporales."""
    partes = []

    try:
        faiss_file = DB_DIR / "index.faiss"
        if faiss_file.exists() and (DB_DIR / "index.pkl").exists():
            embeddings = get_embeddings()
            vectorstore = FAISS.load_local(str(DB_DIR), embeddings, allow_dangerous_deserialization=True)
            if vectorstore.index is not None and vectorstore.index.ntotal > 0:
                resultados = vectorstore.similarity_search(query, k=k)
                if resultados:
                    partes.append("\n\n".join([f"--- FRAGMENTO DE LA NORMA OFICIAL ---\n{doc.page_content}" for doc in resultados]))
    except Exception:
        pass

    if incluir_uploads:
        try:
            faiss_file = DB_UPLOADS_DIR / "index.faiss"
            if faiss_file.exists() and (DB_UPLOADS_DIR / "index.pkl").exists():
                embeddings = get_embeddings()
                vectorstore = FAISS.load_local(str(DB_UPLOADS_DIR), embeddings, allow_dangerous_deserialization=True)
                if vectorstore.index is not None and vectorstore.index.ntotal > 0:
                    resultados = vectorstore.similarity_search(query, k=k)
                    if resultados:
                        partes.append("\n\n".join([f"--- FRAGMENTO DE DOCUMENTO SUBIDO ---\n{doc.page_content}" for doc in resultados]))
        except Exception:
            pass

    return "\n\n".join(partes)

def base_conocimiento_activa() -> bool:
    return DB_DIR.exists() and (DB_DIR / "index.faiss").exists()

def base_uploads_activa() -> bool:
    return DB_UPLOADS_DIR.exists() and (DB_UPLOADS_DIR / "index.faiss").exists()
