import os
import json
import tempfile
from pathlib import Path


class TestFallbackRAG:
    def test_fallback_save_and_load(self):
        from rag_knowledge import _save_fallback, _load_fallback, _split_records, _rank_matches

        docs = [
            {"content": "ISO 27001 control A.9.1.2 acceso a redes", "metadata": {"source": "test.pdf"}},
            {"content": "NIST AI RMF govern 1.0 risk management", "metadata": {"source": "test.pdf"}},
        ]
        tag = "_test_tag"
        _save_fallback(tag, [type("Doc", (), {"page_content": d["content"], "metadata": d["metadata"]})() for d in docs])

        loaded = _load_fallback(tag)
        assert len(loaded) == 2
        assert loaded[0]["content"] == docs[0]["content"]

        chunks = _split_records(loaded)
        assert len(chunks) >= 2

        results = _rank_matches("acceso redes", chunks, k=2)
        assert len(results) >= 1

        import shutil
        shutil.rmtree(Path("data/rag_fallback") / tag, ignore_errors=True)

    def test_obtener_contexto_sin_base(self):
        from rag_knowledge import obtener_contexto
        ctx = obtener_contexto("test query", k=2)
        assert isinstance(ctx, str)

    def test_base_conocimiento_inactiva_sin_datos(self):
        from rag_knowledge import base_conocimiento_activa
        assert isinstance(base_conocimiento_activa(), bool)

    def test_sincronizar_fuentes_sin_repo(self):
        from rag_knowledge import sincronizar_fuentes_oficiales
        assert sincronizar_fuentes_oficiales() == 0


class TestRAGEdgeCases:
    def test_obtener_contexto_query_vacia(self):
        from rag_knowledge import obtener_contexto
        ctx = obtener_contexto("", k=2)
        assert isinstance(ctx, str)

    def test_rank_matches_empty(self):
        from rag_knowledge import _rank_matches
        assert _rank_matches("query", [], k=4) == []

    def test_split_records_empty(self):
        from rag_knowledge import _split_records
        assert _split_records([]) == []

    def test_split_records_no_content(self):
        from rag_knowledge import _split_records
        assert _split_records([{"content": ""}]) == []
