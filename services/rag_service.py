from rag_knowledge import (
    obtener_contexto as _obtener_contexto,
    indexar_documentos as _indexar_documentos,
    indexar_documentos_temporales as _indexar_uploads,
    base_conocimiento_activa,
    base_uploads_activa,
    listar_uploads as _listar_uploads,
    limpiar_uploads as _limpiar_uploads,
    sincronizar_fuentes_oficiales,
)


def get_context(query, k=4, incluir_uploads=True):
    return _obtener_contexto(query, k, incluir_uploads)


def index_documents():
    return _indexar_documentos()


def index_uploads():
    return _indexar_uploads()


def is_knowledge_base_active():
    return base_conocimiento_activa()


def is_uploads_active():
    return base_uploads_activa()


def list_uploads():
    return _listar_uploads()


def clear_uploads():
    return _limpiar_uploads()


def sync_sources():
    return sincronizar_fuentes_oficiales()
