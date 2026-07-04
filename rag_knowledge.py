"""
Módulo RAG (Retrieval-Augmented Generation)
Retorno simple por JSON plano si FAISS falla, para no depender de un solo motor.
"""
import os
import json
import shutil
from pathlib import Path

try:
    from langchain_community.document_loaders import PyPDFLoader
    _HAS_PDF = True
except Exception:
    _HAS_PDF = False

try:
    from langchain_community.document_loaders import TextLoader
    _HAS_TXT = True
except Exception:
    _HAS_TXT = False

try:
    from langchain_community.document_loaders import Docx2txtLoader
    _HAS_DOCX = True
except Exception:
    _HAS_DOCX = False

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    _FAISS_OK = True
except Exception:
    _FAISS_OK = False

KB_DIR = Path("knowledge_base")
UPLOADS_DIR = Path("uploads")
DB_DIR = Path("data/faiss_index")
DB_UPLOADS_DIR = Path("data/faiss_index_uploads")
FALLBACK_DIR = Path("data/rag_fallback")

KB_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
DB_DIR.parent.mkdir(exist_ok=True)
DB_UPLOADS_DIR.parent.mkdir(exist_ok=True)
FALLBACK_DIR.mkdir(exist_ok=True)
FALLBACK_DIR.joinpath("official").mkdir(exist_ok=True)
FALLBACK_DIR.joinpath("uploads").mkdir(exist_ok=True)

# ── Descarga automática desde repositorio de GitHub ─────────────────────────
_KB_REPO = os.getenv("KB_REPO", "").strip()

def sincronizar_fuentes_oficiales():
    """Descarga PDFs desde un repositorio de GitHub a knowledge_base/."""
    if not _KB_REPO or "/" not in _KB_REPO:
        return 0
    owner, repo = _KB_REPO.split("/", 1)
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        import requests
    except Exception:
        return 0

    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return 0
        items = r.json()
        if not isinstance(items, list):
            return 0
        descargados = 0
        for item in items:
            if item.get("type") != "file":
                continue
            name = item.get("name", "")
            if not name.lower().endswith(".pdf"):
                continue
            destino = KB_DIR / name
            if destino.exists():
                continue
            raw_url = item.get("download_url")
            if not raw_url:
                continue
            try:
                pdf_r = requests.get(raw_url, headers=headers, timeout=60)
                if pdf_r.status_code == 200:
                    destino.write_bytes(pdf_r.content)
                    descargados += 1
            except Exception:
                continue
        return descargados
    except Exception:
        return 0

_embeddings_model = None

def get_embeddings():
    global _embeddings_model
    if _embeddings_model is None:
        if not _FAISS_OK:
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
    if suffix == ".txt" and _HAS_TXT:
        return TextLoader(str(archivo), encoding="utf-8").load()
    if suffix == ".docx" and _HAS_DOCX:
        return Docx2txtLoader(str(archivo)).load()
    return []


def _save_fallback(tag: str, documentos):
    carpeta = FALLBACK_DIR / tag
    if carpeta.exists():
        shutil.rmtree(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    payload = []
    for doc in documentos:
        payload.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
        })
    with open(carpeta / "docs.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _load_fallback(tag: str):
    ruta = FALLBACK_DIR / tag / "docs.json"
    if not ruta.exists():
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def _split_records(records):
    out = []
    for record in records:
        content = record.get("content", "")
        if not content:
            continue
        parts = content.split("\n\n")
        for part in parts:
            text = part.strip()
            if text:
                out.append({
                    "content": text,
                    "metadata": record.get("metadata", {}),
                })
    return out


def _rank_matches(query: str, chunks: list, k: int = 4):
    query_lower = query.lower()
    scored = []
    for item in chunks:
        content = item.get("content", "")
        score = 0
        for token in query_lower.split():
            if token in content.lower():
                score += 1
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for _, item in scored[:k]:
        if item.get("content"):
            results.append(item["content"])
    return results


def _try_build_faiss(documentos, destino: Path):
    if not _FAISS_OK or not documentos:
        return False
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documentos)
    if not chunks:
        return False
    try:
        embeddings = get_embeddings()
        textos = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        vectorstore = FAISS.from_texts(textos, embeddings, metadatas=metadatas)
        if destino.exists():
            shutil.rmtree(destino)
        vectorstore.save_local(str(destino))
        return True
    except Exception:
        return False


def indexar_documentos():
    if not _HAS_PDF and not _HAS_TXT and not _HAS_DOCX:
        return 0, "RAG no disponible: faltan loaders de documentos."

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

    try:
        ok = _try_build_faiss(documentos, DB_DIR)
    except Exception as e:
        ok = False
        errores.append(f"FAISS: {e}")

    _save_fallback("official", documentos)
    msg = "Base oficial indexada."
    if ok:
        msg += " Índice FAISS generado."
    else:
        msg += " Se usará búsqueda por fragmentos."
    if errores:
        msg += " Detalles: " + "; ".join(errores)
    return len(documentos), msg


def indexar_documentos_temporales():
    if not _HAS_PDF and not _HAS_TXT and not _HAS_DOCX:
        return 0, "RAG no disponible: faltan loaders de documentos."

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
        return 0, "No se pudo extraer texto. Detalles: " + "; ".join(errores)

    try:
        ok = _try_build_faiss(documentos, DB_UPLOADS_DIR)
    except Exception as e:
        ok = False
        errores.append(f"FAISS: {e}")

    _save_fallback("uploads", documentos)
    msg = "Uploads indexados."
    if ok:
        msg += " Índice FAISS generado."
    else:
        msg += " Se usará búsqueda por fragmentos."
    if errores:
        msg += " Detalles: " + "; ".join(errores)
    return len(documentos), msg


def listar_uploads():
    return sorted(UPLOADS_DIR.glob("*")) if UPLOADS_DIR.exists() else []


def limpiar_uploads():
    if UPLOADS_DIR.exists():
        for archivo in UPLOADS_DIR.glob("*"):
            if archivo.is_file():
                archivo.unlink()
    if DB_UPLOADS_DIR.exists():
        shutil.rmtree(DB_UPLOADS_DIR)
    fallback = FALLBACK_DIR / "uploads"
    if fallback.exists():
        shutil.rmtree(fallback)
    return True


def _obtener_contexto_faiss(ruta_db: Path, query: str, k: int):
    try:
        faiss_file = ruta_db / "index.faiss"
        pkl_file = ruta_db / "index.pkl"
        if not faiss_file.exists() or not pkl_file.exists():
            return []
        embeddings = get_embeddings()
        vectorstore = FAISS.load_local(str(ruta_db), embeddings, allow_dangerous_deserialization=True)
        if vectorstore.index is None or vectorstore.index.ntotal == 0:
            return []
        resultados = vectorstore.similarity_search(query, k=k)
        if resultados:
            return [doc.page_content for doc in resultados]
    except Exception:
        return []
    return []


def _obtener_contexto_fallback(tag: str, query: str, k: int):
    registros = _load_fallback(tag)
    if not registros:
        return []
    chunks = _split_records(registros)
    return _rank_matches(query, chunks, k)


def obtener_contexto(query: str, k: int = 4, incluir_uploads: bool = True) -> str:
    partes = []
    faiss_ok = _obtener_contexto_faiss(DB_DIR, query, k)
    if faiss_ok:
        partes.extend(faiss_ok)
    else:
        fallback = _obtener_contexto_fallback("official", query, k)
        if fallback:
            partes.extend(fallback)

    if incluir_uploads:
        faiss_up = _obtener_contexto_faiss(DB_UPLOADS_DIR, query, k)
        if faiss_up:
            partes.extend(faiss_up)
        else:
            fallback_up = _obtener_contexto_fallback("uploads", query, k)
            if fallback_up:
                partes.extend(fallback_up)

    if partes:
        return "\n\n".join([f"--- FRAGMENTO ---\n{texto}" for texto in partes])
    return ""


def base_conocimiento_activa() -> bool:
    try:
        return (DB_DIR.exists() and (DB_DIR / "index.faiss").exists()) or (FALLBACK_DIR / "official" / "docs.json").exists()
    except Exception:
        return False


def base_uploads_activa() -> bool:
    try:
        return (DB_UPLOADS_DIR.exists() and (DB_UPLOADS_DIR / "index.faiss").exists()) or (FALLBACK_DIR / "uploads" / "docs.json").exists()
    except Exception:
        return False
