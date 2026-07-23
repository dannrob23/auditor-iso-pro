"""
Módulo RAG (Retrieval-Augmented Generation) ligero
Usa sklearn TfidfVectorizer + pypdf — SIN torch, SIN sentence-transformers, SIN FAISS
"""
import os
import json
import shutil
import re
import math
from pathlib import Path
from collections import Counter

try:
    import pypdf
    _HAS_PDF = True
except Exception:
    _HAS_PDF = False

try:
    from docx2txt import process as docx_process
    _HAS_DOCX = True
except Exception:
    _HAS_DOCX = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    _TFIDF_OK = True
except Exception:
    _TFIDF_OK = False

KB_DIR = Path("knowledge_base")
UPLOADS_DIR = Path("uploads")
INDEX_DIR = Path("data/rag_index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)
KB_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)


# ── 1. Extraer texto de archivos ──────────────────────────────────────────────

def _extraer_texto_pdf(ruta: Path) -> str:
    """Extrae texto de un PDF usando pypdf. Ignora archivos corruptos."""
    try:
        lector = pypdf.PdfReader(str(ruta))
        # Verificación rápida: si el PDF está corrupto, lanza error
        num_paginas = len(lector.pages)
        texto = []
        for pagina in lector.pages:
            t = pagina.extract_text()
            if t:
                texto.append(t)
        resultado = "\n".join(texto)
        if len(resultado) < 50:  # Muy poco texto = PDF probablemente corrupto o escaneado
            return ""
        return resultado
    except Exception as e:
        print(f"[RAG] PDF ignorado (corrupto o no parseable): {ruta.name} - {e}")
        return ""


def _extraer_texto_txt(ruta: Path) -> str:
    try:
        return ruta.read_text(encoding="utf-8")
    except Exception:
        return ""


def _extraer_texto_docx(ruta: Path) -> str:
    try:
        from docx2txt import process
        return process(str(ruta))
    except Exception:
        return ""


def _archivos_indexables(directorio: Path):
    archivos = []
    if _HAS_PDF:
        archivos.extend(directorio.glob("*.pdf"))
    archivos.extend(directorio.glob("*.txt"))
    if _HAS_DOCX:
        archivos.extend(directorio.glob("*.docx"))
    return archivos


def _cargar_texto(archivo: Path) -> str:
    suffix = archivo.suffix.lower()
    if suffix == ".pdf":
        return _extraer_texto_pdf(archivo)
    elif suffix == ".txt":
        return _extraer_texto_txt(archivo)
    elif suffix == ".docx":
        return _extraer_texto_docx(archivo)
    return ""


# ── 2. Indexar documentos usando TF-IDF ──────────────────────────────────────

def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Divide texto en fragmentos solapados."""
    words = text.split()
    chunks = []
    if not words:
        return chunks
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks


def _indexar_directorio(directorio: Path) -> dict:
    """Indexa documentos de un directorio usando TF-IDF."""
    archivos = _archivos_indexables(directorio)
    if not archivos:
        return {}

    todos_chunks = []
    metadatos = []

    for archivo in archivos:
        texto = _cargar_texto(archivo)
        if not texto:
            continue
        chunks = _chunk_text(texto)
        for chunk in chunks:
            todos_chunks.append(chunk)
            metadatos.append({
                "archivo": archivo.name,
                "ruta": str(archivo),
            })

    if not todos_chunks or not _TFIDF_OK:
        return {}

    try:
        vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words=["el", "la", "los", "las", "de", "del", "en", "y", "a", "que",
                        "es", "por", "con", "para", "un", "una", "su", "al", "lo",
                        "como", "más", "pero", "sus", "le", "ya", "este", "entre",
                        "todo", "esta", "sin", "son", "ser", "ha", "dos", "tiene",
                        "también", "era", "muy", "ese", "sino", "cada", "les",
                        "puede", "todos", "cual", "sea", "ello", "durante", "así",
                        "sí", "ello", "este", "otro", "eso", "ni", "no", "se"],
            min_df=1,
            max_df=0.85,
        )
        tfidf_matrix = vectorizer.fit_transform(todos_chunks)

        index_data = {
            "todos_chunks": todos_chunks,
            "metadatos": metadatos,
            "vocab": vectorizer.get_feature_names_out().tolist(),
            "idf": vectorizer.idf_.tolist(),
        }
        return index_data
    except Exception:
        return {}


def _save_index(tag: str, index_data: dict):
    """Guarda el índice TF-IDF como JSON."""
    carpeta = INDEX_DIR / tag
    if carpeta.exists():
        shutil.rmtree(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    payload = {
        "todos_chunks": index_data["todos_chunks"],
        "metadatos": index_data["metadatos"],
        "vocab": index_data["vocab"],
        "idf": index_data["idf"],
    }
    with open(carpeta / "index.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    print(f"[RAG] Índice guardado: {carpeta}")


def _load_index(tag: str) -> dict | None:
    """Carga un índice TF-IDF guardado."""
    ruta = INDEX_DIR / tag / "index.json"
    if not ruta.exists():
        return None
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# ── 3. Búsqueda semántica ─────────────────────────────────────────────────────

def _buscar_index(index_data: dict, query: str, k: int = 4) -> list[str]:
    """Busca en el índice TF-IDF usando similitud coseno."""
    if not index_data or not _TFIDF_OK:
        return []

    todos_chunks = index_data["todos_chunks"]
    metadatos = index_data["metadatos"]
    vocab = index_data["vocab"]
    idf = index_data["idf"]

    if not todos_chunks:
        return []

    try:
        vectorizer = TfidfVectorizer(
            vocabulary=vocab,
        )
        vectorizer.idf_ = np.array(idf)
        tfidf_matrix = vectorizer.fit_transform(todos_chunks)

        query_vec = vectorizer.transform([query])
        similitudes = cosine_similarity(query_vec, tfidf_matrix).flatten()
        indices_top = similitudes.argsort()[-k:][::-1]

        resultados = []
        for idx in indices_top:
            if similitudes[idx] > 0.01:  # Umbral mínimo de relevancia
                fuente = metadatos[idx]["archivo"] if idx < len(metadatos) else "Desconocido"
                resultados.append(
                    f"[Fuente: {fuente}]\n{todos_chunks[idx][:500]}"
                )
        return resultados
    except Exception as e:
        print(f"[RAG] Error en búsqueda: {e}")
        return []


def _buscar_fallback(query: str, index_data: dict, k: int = 4) -> list[str]:
    """Fallback: búsqueda por palabras clave sin TF-IDF."""
    if not index_data:
        return []
    todos_chunks = index_data.get("todos_chunks", [])
    metadatos = index_data.get("metadatos", [])
    if not todos_chunks:
        return []

    query_lower = query.lower()
    tokens_query = [t for t in query_lower.split() if len(t) > 3]

    scored = []
    for i, chunk in enumerate(todos_chunks):
        chunk_lower = chunk.lower()
        score = sum(1 for t in tokens_query if t in chunk_lower)
        if score > 0:
            fuente = metadatos[i]["archivo"] if i < len(metadatos) else "Desconocido"
            scored.append((score, i, fuente))

    scored.sort(key=lambda x: x[0], reverse=True)
    resultados = []
    for _, idx, fuente in scored[:k]:
        resultados.append(f"[Fuente: {fuente}]\n{todos_chunks[idx][:500]}")
    return resultados


# ── 4. API pública ────────────────────────────────────────────────────────────

def indexar_documentos() -> tuple[int, str]:
    """Indexa los documentos de knowledge_base/."""
    if not _HAS_PDF:
        return 0, "RAG no disponible: faltan dependencias (pypdf)."

    index_data = _indexar_directorio(KB_DIR)
    if not index_data:
        return 0, "No se encontraron documentos indexables en knowledge_base/."

    total_chunks = len(index_data["todos_chunks"])
    _save_index("official", index_data)
    return total_chunks, f"Base de conocimiento indexada: {total_chunks} fragmentos de documentos ISO/NIST."


def indexar_documentos_temporales() -> tuple[int, str]:
    """Indexa los documentos subidos por el usuario."""
    if not _HAS_PDF:
        return 0, "RAG no disponible: faltan dependencias (pypdf)."

    index_data = _indexar_directorio(UPLOADS_DIR)
    if not index_data:
        return 0, "No se encontraron archivos en uploads/."

    total_chunks = len(index_data["todos_chunks"])
    _save_index("uploads", index_data)
    return total_chunks, f"Uploads indexados: {total_chunks} fragmentos."


def obtener_contexto(query: str, k: int = 4, incluir_uploads: bool = True) -> str:
    """Obtiene contexto relevante de la base de conocimiento."""
    partes = []

    # Buscar en documentos oficiales
    index_data = _load_index("official")
    if index_data:
        if _TFIDF_OK:
            resultados = _buscar_index(index_data, query, k)
        else:
            resultados = _buscar_fallback(query, index_data, k)
        if resultados:
            partes.extend(resultados)

    # Buscar en uploads si aplica
    if incluir_uploads:
        index_up = _load_index("uploads")
        if index_up:
            if _TFIDF_OK:
                resultados = _buscar_index(index_up, query, k)
            else:
                resultados = _buscar_fallback(query, index_up, k)
            if resultados:
                partes.extend(resultados)

    if partes:
        return "\n\n---\n".join(partes)
    return ""


def base_conocimiento_activa() -> bool:
    """Verifica si hay documentos indexados disponibles."""
    index_path = INDEX_DIR / "official" / "index.json"
    return index_path.exists()


def base_uploads_activa() -> bool:
    index_path = INDEX_DIR / "uploads" / "index.json"
    return index_path.exists()


def listar_uploads() -> list:
    return sorted(UPLOADS_DIR.glob("*")) if UPLOADS_DIR.exists() else []


def limpiar_uploads():
    if UPLOADS_DIR.exists():
        for archivo in UPLOADS_DIR.glob("*"):
            if archivo.is_file():
                archivo.unlink()
    upload_index = INDEX_DIR / "uploads"
    if upload_index.exists():
        shutil.rmtree(upload_index)
    return True


def sincronizar_fuentes_oficiales():
    """Descarga PDFs desde GitHub Releases a knowledge_base/."""
    url = "https://github.com/dannrob23/auditor-iso-pro/releases/download/knowledge/knowledge_base_pdfs.zip"
    try:
        import requests, zipfile, io
        if any(KB_DIR.glob("*.pdf")):
            return 0
        r = requests.get(url, timeout=120)
        if r.status_code != 200:
            return 0
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for member in z.namelist():
                if member.endswith(".pdf"):
                    target = KB_DIR / member.split("/")[-1]
                    target.write_bytes(z.read(member))
        return len(list(KB_DIR.glob("*.pdf")))
    except Exception:
        return 0
