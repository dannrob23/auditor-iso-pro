"""
Embeddings para RAG.
Usa TF-IDF (sklearn) por defecto — sin API, sin costo, sin torch.
Opcional: OpenAI text-embedding-3-small si está configurado.
"""
import os
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def _get_tfidf_vectors(texts: list[str]) -> np.ndarray:
    """Genera vectores TF-IDF localmente (sin API, sin costo)."""
    if not texts:
        return np.array([], dtype=np.float32)
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
        sublinear_tf=True,
    )
    matrix = vectorizer.fit_transform(texts)
    # Convertir a dense y normalizar para cosine similarity
    result = matrix.toarray().astype(np.float32)
    norms = np.linalg.norm(result, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return result / norms


def _get_openai_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> np.ndarray:
    """Embeddings vía OpenAI API. Solo si hay OPENAI_API_KEY."""
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurada.")
    client = OpenAI(api_key=api_key)

    batch_size = 100
    all_vectors = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_clean = [t[:30000] for t in batch]
        for intento in range(3):
            try:
                resp = client.embeddings.create(input=batch_clean, model=model)
                vectors = [item.embedding for item in resp.data]
                all_vectors.extend(vectors)
                break
            except Exception as e:
                if intento < 2:
                    time.sleep(2 ** intento)
                else:
                    raise RuntimeError(f"Embeddings OpenAI fallaron: {e}")

    result = np.array(all_vectors, dtype=np.float32)
    norms = np.linalg.norm(result, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return result / norms


# ── Router principal ──

def get_embeddings(texts: list[str], provider: str | None = None) -> np.ndarray:
    """
    Genera vectores para una lista de textos.
    
    Prioridad:
    1. OpenAI (si hay OPENAI_API_KEY) — embeddings semánticos (mejor calidad)
    2. TF-IDF local (siempre disponible) — palabras clave (sin costo)

    Args:
        texts: Lista de textos a vectorizar
        provider: "openai", "tfidf", o None (autodetecta)

    Returns:
        np.ndarray float32 normalizado (L2).
    """
    if not texts:
        return np.array([], dtype=np.float32)

    errores = []

    # Intentar OpenAI si hay key y no se forzó TF-IDF
    if provider != "tfidf" and os.getenv("OPENAI_API_KEY"):
        try:
            return _get_openai_embeddings(texts)
        except Exception as e:
            errores.append(f"OpenAI: {e}")

    # TF-IDF local (siempre funciona, sin costo)
    if provider != "openai":
        print("[Embeddings] Usando TF-IDF local (sin API)")
        return _get_tfidf_vectors(texts)

    raise RuntimeError(f"No se pudieron generar embeddings. {'; '.join(errores)}")


def embedding_dim(provider: str = "tfidf") -> int:
    """Dimensión de los vectores. TF-IDF usa max_features=5000."""
    if provider == "openai":
        return 1536
    return 5000  # TF-IDF default max_features
