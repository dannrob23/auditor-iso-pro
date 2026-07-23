"""
Embeddings via API para RAG.
Genera vectores usando DeepSeek API (compatible con OpenAI embeddings).
SIN torch, SIN sentence-transformers, SIN modelos locales.
Costo: DEEPSEEK_API_KEY ya la tienes configurada.
"""
import os
import time
import numpy as np


def _get_deepseek_embeddings(texts: list[str], model: str = "deepseek-chat") -> np.ndarray:
    """
    Genera embeddings vía DeepSeek API (compatible con OpenAI).
    DeepSeek no cobra extra por embeddings — mismo costo que chat normal.
    """
    import openai
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY no configurada. RAG no disponible.")

    client = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

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
                    raise RuntimeError(f"Embeddings DeepSeek fallaron: {e}")

    if not all_vectors:
        raise RuntimeError("No se generaron embeddings.")

    result = np.array(all_vectors, dtype=np.float32)
    # Normalizar L2 para cosine similarity
    norms = np.linalg.norm(result, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return result / norms


# ── Proveedores alternativos (fallback) ──

def _get_openai_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> np.ndarray:
    """Fallback: embeddings vía OpenAI API."""
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


def _get_google_embeddings(texts: list[str]) -> np.ndarray:
    """Fallback: embeddings vía Google Gemini API."""
    import google.genai as genai
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY no configurada.")
    client = genai.Client(api_key=api_key)

    batch_size = 100
    all_vectors = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for intento in range(3):
            try:
                resp = client.models.embed_content(model="text-embedding-004", contents=batch)
                for item in resp.embeddings:
                    all_vectors.append(item.values)
                break
            except Exception as e:
                if intento < 2:
                    time.sleep(2 ** intento)
                else:
                    raise RuntimeError(f"Embeddings Google fallaron: {e}")

    result = np.array(all_vectors, dtype=np.float32)
    norms = np.linalg.norm(result, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return result / norms


# ── Router principal ──

def get_embeddings(texts: list[str], provider: str | None = None) -> np.ndarray:
    """
    Genera embeddings para una lista de textos.
    
    Orden de preferencia:
    1. DeepSeek (ya tienes API key, no paga extra)
    2. OpenAI (fallback si no hay DeepSeek)
    3. Google (fallback si no hay OpenAI)

    Args:
        texts: Lista de textos a vectorizar
        provider: Forzar proveedor ("deepseek", "openai", "google"). 
                  Si es None, autodetecta.

    Returns:
        np.ndarray float32 normalizado (L2).

    Raises:
        RuntimeError: si no hay API key configurada.
    """
    if not texts:
        return np.array([], dtype=np.float32)

    errores = []

    if provider == "deepseek" or (provider is None and os.getenv("DEEPSEEK_API_KEY")):
        try:
            return _get_deepseek_embeddings(texts)
        except Exception as e:
            errores.append(f"DeepSeek: {e}")

    if provider == "openai" or (provider is None and os.getenv("OPENAI_API_KEY")):
        try:
            return _get_openai_embeddings(texts)
        except Exception as e:
            errores.append(f"OpenAI: {e}")

    if provider == "google" or (provider is None and os.getenv("GOOGLE_API_KEY")):
        try:
            return _get_google_embeddings(texts)
        except Exception as e:
            errores.append(f"Google: {e}")

    raise RuntimeError(f"No hay API key configurada para embeddings. Intentos: {'; '.join(errores)}")


def embedding_dim(provider: str = "deepseek") -> int:
    """Dimensión de los vectores según el proveedor."""
    dims = {"deepseek": 2048, "openai": 1536, "google": 768}
    return dims.get(provider, 2048)
