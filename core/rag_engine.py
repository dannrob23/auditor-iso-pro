"""
Motor RAG ligero con FAISS + embeddings por API.
Sin torch, sin sentence-transformers.
"""
import os
import json
import pickle
import time
import threading
from pathlib import Path
import numpy as np

import faiss
from core.embeddings import get_embeddings, embedding_dim
from core.chunking import load_and_chunk_pdfs


# ── Prompt anti-alucinación ───────────────────────────────────────────────────

SYSTEM_PROMPT_RAG = """Eres un auditor experto en ISO/IEC 27001:2022, ISO/IEC 42001:2023, NIST AI RMF 1.0, ISO 19011:2018 e ISO 23894:2023.

REGLAS ABSOLUTAS:
1. SOLO respondes con base en el contexto que está entre las etiquetas <contexto> y </contexto>.
2. Si la respuesta no está en el contexto, dices: "No encontré información específica en las fuentes cargadas para responder esta consulta."
3. NUNCA inventes numerales, cláusulas, controles o requisitos que no aparezcan explícitamente en el contexto.
4. SIEMPRE cita la fuente al final de cada hallazgo con el formato: [Documento | Sección | Relevancia]
5. Distingue claramente entre texto normativo (lo que dice la norma) y tu interpretación como auditor.

Formato de respuesta:
**Hallazgo:** [descripción del hallazgo]
**Fuente normativa:** [Documento, Sección, cita textual relevante]
**Recomendación:** [acción recomendada]
**Nivel de cumplimiento:** [Conforme / Parcial / No conforme / No evaluado]

Contexto disponible:
<contexto>
{contexto_rag}
</contexto>

Pregunta del auditor:
{pregunta}"""

CACHE_DIR = Path("rag_cache")
INDEX_FILE = CACHE_DIR / "index.faiss"
META_FILE = CACHE_DIR / "metadata.pkl"
STATS_FILE = CACHE_DIR / "stats.json"


class RAGEngine:
    """Motor RAG: indexa documentos, busca por similitud semántica vía API embeddings."""

    def __init__(self):
        self._index: faiss.Index | None = None
        self._metadata: list[dict] = []
        self._active = False
        self._provider = "openai"  # fallback a OpenAI
        self._dim = 1536
        self._stats = {"chunks": 0, "sources": [], "size_mb": 0}
        self._lock = threading.Lock()

    # ── Propiedades ──

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def stats(self) -> dict:
        return dict(self._stats)

    @property
    def provider(self) -> str:
        return self._provider

    # ── Construcción del índice ──

    def build_index(self, force: bool = False, kb_dir: str = "knowledge_base") -> bool:
        """
        Construye o carga el índice FAISS desde caché.

        Args:
            force: Si True, fuerza re-indexación ignorando caché
            kb_dir: Directorio con PDFs

        Returns:
            True si el índice está activo, False si falló
        """
        with self._lock:
            # Detectar proveedor disponible
            api_key = os.getenv("OPENAI_API_KEY", "")
            if not api_key:
                api_key = os.getenv("GOOGLE_API_KEY", "")
                if api_key:
                    self._provider = "google"
                    self._dim = 768

            if not api_key:
                print("[RAG] No hay API key para embeddings. RAG desactivado.")
                self._active = False
                return False

            # Cargar desde caché si existe y no se fuerza re-indexación
            if not force and self._load_cache():
                print(f"[RAG] Índice cargado desde caché: {self._stats}")
                return True

            # Indexar desde PDFs
            print("[RAG] Indexando documentos...")
            chunks = load_and_chunk_pdfs(kb_dir)
            if not chunks:
                print("[RAG] No hay chunks para indexar.")
                self._active = False
                return False

            try:
                self._build_from_chunks(chunks)
                self._save_cache()
                print(f"[RAG] Índice construido: {self._stats}")
                return True
            except Exception as e:
                print(f"[RAG] Error construyendo índice: {e}")
                self._active = False
                return False

    def _build_from_chunks(self, chunks: list[dict]):
        """Construye índice FAISS desde una lista de chunks."""
        textos = [c["text"] for c in chunks]

        # Generar embeddings vía API
        vectors = get_embeddings(textos, provider=self._provider)

        # Crear índice FAISS
        dim = vectors.shape[1]
        self._index = faiss.IndexFlatIP(dim)
        self._index.add(vectors)

        self._metadata = chunks
        self._active = True

        # Calcular stats
        self._stats = {
            "chunks": len(chunks),
            "sources": list(set(c["source"] for c in chunks)),
            "size_mb": round(vectors.nbytes / (1024 * 1024), 2),
            "dim": dim,
            "provider": self._provider,
        }

    # ── Búsqueda ──

    def search(self, query: str, top_k: int = 5, threshold: float = 0.35) -> list[dict]:
        """
        Busca los chunks más relevantes para una consulta.

        Args:
            query: Texto de la consulta
            top_k: Número máximo de resultados
            threshold: Umbral mínimo de similitud (cosine)

        Returns:
            List[Dict] con {"text", "source", "section", "score"}
        """
        if not self._active or self._index is None:
            return []

        # Generar embedding de la consulta
        try:
            q_vector = get_embeddings([query], provider=self._provider)
        except Exception as e:
            print(f"[RAG] Error generando embedding de consulta: {e}")
            return []

        # Buscar
        scores, indices = self._index.search(q_vector, top_k)

        resultados = []
        for score, idx in zip(scores[0], indices[0]):
            if score < threshold or idx < 0 or idx >= len(self._metadata):
                continue
            chunk = self._metadata[idx]
            resultados.append({
                "text": chunk["text"][:500],  # Limitar por longitud
                "source": chunk["source"],
                "section": chunk["section"],
                "score": round(float(score), 3),
            })

        return resultados

    def get_context(self, query: str, top_k: int = 5) -> str:
        """
        Obtiene contexto formateado para inyectar en el prompt del LLM.

        Args:
            query: Consulta del usuario
            top_k: Número de fragmentos a recuperar

        Returns:
            String con fragmentos formateados para el prompt
        """
        resultados = self.search(query, top_k=top_k)
        if not resultados:
            return ""

        partes = []
        for i, r in enumerate(resultados, 1):
            texto = r["text"].replace("\n", " ").strip()
            partes.append(
                f"[Fragmento {i}] Fuente: {r['source']} | Sección: {r['section']} | "
                f"Relevancia: {r['score']:.2f}\n{texto}"
            )

        return "\n\n".join(partes)

    # ── Caché ──

    def _save_cache(self):
        """Guarda índice y metadatos a disco."""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        if self._index is not None:
            faiss.write_index(self._index, str(INDEX_FILE))
        with open(META_FILE, "wb") as f:
            pickle.dump(self._metadata, f)
        with open(STATS_FILE, "w") as f:
            json.dump(self._stats, f)

    def _load_cache(self) -> bool:
        """Carga índice y metadatos desde disco."""
        if not INDEX_FILE.exists() or not META_FILE.exists():
            return False
        try:
            self._index = faiss.read_index(str(INDEX_FILE))
            with open(META_FILE, "rb") as f:
                self._metadata = pickle.load(f)
            if STATS_FILE.exists():
                with open(STATS_FILE) as f:
                    self._stats = json.load(f)
            self._active = True
            return True
        except Exception as e:
            print(f"[RAG] Error cargando caché: {e}")
            return False


# ── Singleton global ──────────────────────────────────────────────────────────

_rag_instance = None
_rag_lock = threading.Lock()


def get_rag() -> RAGEngine:
    """Obtiene la instancia singleton del motor RAG."""
    global _rag_instance
    if _rag_instance is None:
        with _rag_lock:
            if _rag_instance is None:
                _rag_instance = RAGEngine()
    return _rag_instance


def init_rag_background(kb_dir: str = "knowledge_base"):
    """Inicializa RAG en un thread background (no bloquea el startup)."""
    def _init():
        engine = get_rag()
        engine.build_index(force=False, kb_dir=kb_dir)

    thread = threading.Thread(target=_init, daemon=True)
    thread.start()
    print("[RAG] Inicialización en background iniciada")


def format_prompt(query: str, contexto: str) -> str:
    """Formatea el prompt completo con contexto RAG para el LLM."""
    return SYSTEM_PROMPT_RAG.format(contexto_rag=contexto or "No hay contexto disponible.", pregunta=query)
