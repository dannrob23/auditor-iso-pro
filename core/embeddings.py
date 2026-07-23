"""
Embeddings via API para RAG.
Genera vectores usando OpenAI text-embedding-3-small o Google text-embedding-004.
SIN torch, SIN sentence-transformers, SIN modelos locales.
"""
import os
import time
import numpy as np
from openai import OpenAI


def _get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _get_google_client():
    try:
        import google.genai as genai
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            return None
        return genai.Client(api_key=api_key)
    except Exception:
        return None


def get_embeddings(texts: list[str], provider: str = "openai", model: str | None = None) -> np.ndarray:
    """
    Genera embeddings para una lista de textos vía API.

    Args:
        texts: Lista de textos a vectorizar
        provider: "openai" (default) o "google"
        model: Modelo de embeddings. OpenAI: "text-embedding-3-small" (default),
               Google: "text-embedding-004"

    Returns:
        np.ndarray de forma (len(texts), dims) con vectores float32 normalizados (L2).

    Raises:
        RuntimeError: si no hay API key configurada o fallan todos los intentos.
    """
    if not texts:
        return np.array([], dtype=np.float32)

    if provider == "google":
        return _get_embeddings_google(texts)
    return _get_embeddings_openai(texts, model or "text-embedding-3-small")


def _get_embeddings_openai(texts: list[str], model: str = "text-embedding-3-small") -> np.ndarray:
    """Embeddings vía OpenAI API con batching y retry."""
    client = _get_openai_client()
    if client is None:
        raise RuntimeError("OPENAI_API_KEY no configurada. RAG vía API requiere OpenAI o Google.")

    batch_size = 100
    all_vectors = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        # Limpiar textos (máx 8192 tokens ≈ 32000 chars)
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
                    raise RuntimeError(f"Embeddings OpenAI fallaron tras 3 intentos: {e}")

    result = np.array(all_vectors, dtype=np.float32)
    # Normalizar L2 (cosine similarity con inner product)
    norms = np.linalg.norm(result, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return result / norms


def _get_embeddings_google(texts: list[str]) -> np.ndarray:
    """Embeddings vía Google Gemini API."""
    client = _get_google_client()
    if client is None:
        raise RuntimeError("GOOGLE_API_KEY no configurada para embeddings.")

    model = "text-embedding-004"
    batch_size = 100
    all_vectors = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for intento in range(3):
            try:
                resp = client.models.embed_content(model=model, contents=batch)
                for item in resp.embeddings:
                    all_vectors.append(item.values)
                break
            except Exception as e:
                if intento < 2:
                    time.sleep(2 ** intento)
                else:
                    raise RuntimeError(f"Embeddings Google fallaron tras 3 intentos: {e}")

    result = np.array(all_vectors, dtype=np.float32)
    norms = np.linalg.norm(result, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return result / norms


def embedding_dim(provider: str = "openai") -> int:
    """Dimensión de los vectores según el proveedor."""
    return 1536 if provider == "openai" else 768
