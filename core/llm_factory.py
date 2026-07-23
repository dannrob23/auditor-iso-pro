import os
import io
import pypdf
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# ── Helper RAG ───────────────────────────────────────────────────────────────

def _obtener_contexto_rag(consulta: str, k: int = 4) -> tuple[str, bool]:
    """Obtiene contexto de las normas vía RAG TF-IDF (sin API)."""
    try:
        from core.rag_engine import get_rag
        engine = get_rag()
        if engine.is_active:
            ctx = engine.get_context(consulta, top_k=k)
            return ctx, bool(ctx)
        return "", False
    except Exception:
        return "", False


def _formatear_contexto(contexto: str, activo: bool, solicitado: bool) -> str:
    """Formatea el contexto RAG para inyectar en el prompt del LLM."""
    if contexto:
        return (f"\n\n--- INICIO CONTEXTO NORMATIVO (RAG) ---\n{contexto}\n--- FIN CONTEXTO ---\n"
                "Utiliza exclusivamente el contexto anterior para fundamentar tu respuesta. "
                "CITA la fuente de cada referencia [Documento | Sección].")
    if solicitado and not activo:
        return ("\n\nNota: Base de conocimiento RAG no disponible. "
                "Responde con tu conocimiento general, pero INDICA que no tienes las normas oficiales para confirmar.")
    return ""


# ── LLM Factory ──────────────────────────────────────────────────────────────

def _construir_llm(proveedor: str, modelo_llm: str, temp: float):
    """Construye el objeto LLM según proveedor. Lanza ValueError si falta API key."""
    if proveedor == "Google (Gemini)":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("No se encontró GOOGLE_API_KEY en .env")
        return ChatGoogleGenerativeAI(model=modelo_llm, temperature=temp, google_api_key=api_key)
    elif proveedor == "DeepSeek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("No se encontró DEEPSEEK_API_KEY en .env")
        return ChatOpenAI(model=modelo_llm, temperature=temp, api_key=api_key, base_url="https://api.deepseek.com/v1")
    elif proveedor == "Groq (Gratis)":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("No se encontró GROQ_API_KEY en .env")
        return ChatOpenAI(model=modelo_llm, temperature=temp, api_key=api_key, base_url="https://api.groq.com/openai/v1")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró OPENAI_API_KEY en .env")
        return ChatOpenAI(model=modelo_llm, temperature=temp, api_key=api_key)


def extraer_texto_pdf(archivo) -> str:
    archivo.seek(0)
    lector = pypdf.PdfReader(io.BytesIO(archivo.read()))
    texto = ""
    for pagina in lector.pages:
        texto += pagina.extract_text() or ""
    return texto.strip()


# ── Gap Analysis (con RAG) ───────────────────────────────────────────────────

def ejecutar_gap_analysis(texto_politica: str, proveedor: str, modelo_llm: str, temp: float, usar_rag: bool = True) -> str:
    system_prompt = """Eres un Auditor Líder ISO/IEC 27001:2022, ISO/IEC 42001:2023, NIST AI RMF 1.0, ISO 19011:2018 e ISO 23894:2023.

Debes realizar un GAP ANALYSIS comparando el documento de política proporcionado contra los requisitos de los 5 marcos normativos.

REGLAS:
1. Identifica qué controles/requisitos CUMPLE, cuáles NO, y cuáles están PARCIALMENTE implementados.
2. Si el contexto normativo (RAG) está disponible, úsalo para CITAR textualmente las secciones relevantes.
3. Si NO hay contexto RAG, usa tu conocimiento pero INDÍCALO.
4. Asigna un nivel de cumplimiento: CONFORME / PARCIAL / NO CONFORME / NO EVALUADO.

INSTRUCCIONES DE FORMATO:
- Responde ÚNICAMENTE con una tabla Markdown con exactamente 4 columnas:
  | Control / Requisito (Marco Confluente) | Estado | Observación Técnica (Infraestructura Crítica) | Acción de Mejora |
- Al final, agrega un RESUMEN EJECUTIVO de confluencia."""

    # RAG: Extraer contexto de las normas
    contexto, activo = _obtener_contexto_rag(texto_politica[:1500], k=4) if usar_rag else ("", False)
    contexto_texto = _formatear_contexto(contexto, activo, usar_rag)

    user_prompt = f"""Ejecuta el Gap Analysis sobre el siguiente documento de política de seguridad:

---INICIO DEL DOCUMENTO DE POLÍTICA---
{texto_politica}
---FIN DEL DOCUMENTO DE POLÍTICA---{contexto_texto}

Genera la tabla de Gap Analysis ISO/IEC 27001:2022 completa."""

    mensajes = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    try:
        llm = _construir_llm(proveedor, modelo_llm, temp)
        respuesta = llm.invoke(mensajes)
        return respuesta.content
    except ValueError as e:
        return f"⚠️ Error de configuración: {e}"
    except Exception as e:
        return f"⚠️ Error al generar gap analysis: {e}"


# ── Chat Auditor (con RAG) ───────────────────────────────────────────────────

def ejecutar_chat(mensajes_historial: list, proveedor: str, modelo_llm: str, temp: float, usar_rag: bool = True):
    try:
        llm = _construir_llm(proveedor, modelo_llm, temp)
    except ValueError as e:
        return f"⚠️ Error de configuración: {e}"

    system_prompt = SystemMessage(
        content="Eres un Auditor experto en ISO/IEC 27001:2022, ISO/IEC 42001:2023, NIST AI RMF 1.0, "
                "ISO 19011:2018 e ISO 23894:2023.\n\n"
                "IMPORTANTE:\n"
                "- Si el usuario te pregunta sobre normas, controles o requisitos, fundamenta tu respuesta "
                "en el contexto normativo disponible.\n"
                "- Si no tienes el contexto de una norma específica, INDÍCALO claramente.\n"
                "- NUNCA inventes numerales, cláusulas o controles.\n"
                "- Responde de forma profesional y técnica como un Auditor Líder."
    )

    # Si es una pregunta nueva y usar_rag está activo, buscar contexto
    formatted_messages = [system_prompt]
    ultimo_mensaje = ""
    for m in mensajes_historial:
        if m["role"] == "user":
            ultimo_mensaje = m["content"]
            formatted_messages.append(HumanMessage(content=m["content"]))
        else:
            formatted_messages.append(AIMessage(content=m["content"]))

    # Inyectar contexto RAG en el último mensaje del usuario si aplica
    if usar_rag and ultimo_mensaje:
        contexto, activo = _obtener_contexto_rag(ultimo_mensaje[:1500], k=3)
        if contexto:
            # Insertar mensaje de sistema con el contexto justo antes del último mensaje
            contexto_msg = SystemMessage(
                content=f"Contexto normativo relevante para la pregunta del auditor:\n{contexto}\n\n"
                        "Usa este contexto para fundamentar tu respuesta. CITA cada fuente."
            )
            formatted_messages.insert(-1, contexto_msg)

    try:
        respuesta = llm.invoke(formatted_messages)
        return respuesta.content
    except Exception as e:
        return f"⚠️ El asistente no pudo responder: {e}"
