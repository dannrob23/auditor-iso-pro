import streamlit as st
import yaml
import os
import sys
import json as _json
import subprocess
import traceback
from pathlib import Path
from yaml.loader import SafeLoader
from dotenv import load_dotenv
import streamlit_authenticator as stauth
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import pypdf
import io
import sqlite3
from audit_logger import log_event, get_log_entries
from database import (
    guardar_reporte, listar_reportes, obtener_reporte, stats_globales, init_db,
    guardar_lote_vulnerabilidades, listar_vulnerabilidades, stats_vulnerabilidades,
    guardar_vulnerabilidad, limpiar_vulnerabilidades_antiguas, exportar_excel_respaldo,
    crear_auditoria, obtener_auditorias, obtener_auditoria, actualizar_auditoria,
)
from pdf_export import (
    generar_pdf,
    generar_pdf_propuesta_interoperabilidad,
)
from guia_auditoria import (
    ETAPAS, SECTORES_EMPRESA, TAMANOS_EMPRESA,
    obtener_controles_recomendados, generar_plan_implementacion,
    generar_reporte_markdown, etapa_icono_estado, avanzar_etapa,
)

try:
    from core.rag_engine import get_rag

    def obtener_contexto(query: str, k: int = 4) -> str:
        engine = get_rag()
        return engine.get_context(query, top_k=k)

    def indexar_documentos():
        engine = get_rag()
        ok = engine.build_index(force=True)
        if ok:
            stats = engine.stats
            return stats["chunks"], f"Índice RAG reconstruido: {stats['chunks']} fragmentos de {len(stats['sources'])} fuentes."
        return 0, "No se pudo indexar. Verifica knowledge_base/ y API key."

    def base_conocimiento_activa() -> bool:
        return get_rag().is_active

    def listar_uploads():
        return []

    def limpiar_uploads():
        return True

    def base_uploads_activa():
        return False

    def indexar_documentos_temporales():
        return 0, "Función temporal deshabilitada en RAG vía API."

    _RAG_AVAILABLE = True
except Exception:
    _RAG_AVAILABLE = False
    def obtener_contexto(query: str, k: int = 4) -> str:
        return ''
    def indexar_documentos():
        return 0, 'RAG no disponible'
    def base_conocimiento_activa():
        return False
    def listar_uploads():
        return []
    def limpiar_uploads():
        return True
    def base_uploads_activa():
        return False
    def indexar_documentos_temporales():
        return 0, 'RAG no disponible'

from interoperabilidad import (
    MATRIZ_INTEROPERABILIDAD, SECTORES_IC, obtener_dimensiones,
    obtener_controles_por_dimension, calcular_cobertura, obtener_sector,
    generar_resumen_interoperabilidad, generar_propuesta_ic, generar_markdown_matriz,
    generar_df_interoperabilidad, calcular_cumplimiento, exportar_matriz_excel
)
from ingestor import (
    fetch_all, fetch_avid_reports, fetch_mitre_atlas, fetch_mit_risk_repo,
    analizar_vulnerabilidad, normalize_batch, set_provider, MODEL_MAP,
    calcular_riesgo, criticidad_compuesta, resumen_estadistico, clasificar_tactica,
    CUESTIONARIO_CONTEXTO, generar_prompt_contexto,
    exportar_matriz_riesgos_ia,
)
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timezone, timedelta

BOGOTA_OFFSET = timedelta(hours=-5)

def ahora_bogota():
    return datetime.now(timezone.utc) + BOGOTA_OFFSET
