import os
import io
import pypdf
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


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


def ejecutar_gap_analysis(texto_politica: str, proveedor: str, modelo_llm: str, temp: float, usar_rag: bool = True) -> str:
    if proveedor == "Google (Gemini)":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "ERROR: No se encontró GOOGLE_API_KEY en el archivo .env"
        llm = ChatGoogleGenerativeAI(model=modelo_llm, temperature=temp, google_api_key=api_key)
    elif proveedor == "DeepSeek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return "ERROR: No se encontró DEEPSEEK_API_KEY en el archivo .env"
        llm = ChatOpenAI(model=modelo_llm, temperature=temp, api_key=api_key, base_url="https://api.deepseek.com/v1")
    elif proveedor == "Groq (Gratis)":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "ERROR: No se encontró GROQ_API_KEY en el archivo .env"
        llm = ChatOpenAI(model=modelo_llm, temperature=temp, api_key=api_key, base_url="https://api.groq.com/openai/v1")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "ERROR: No se encontró OPENAI_API_KEY en el archivo .env"
        llm = ChatOpenAI(model=modelo_llm, temperature=temp, api_key=api_key)

    system_prompt = """Eres un Auditor Líder experto en Ciberseguridad e Inteligencia Artificial, con dominio profundo de ISO/IEC 27001:2022, NIST AI RMF 1.0 e ISO/IEC 42001:2023.
Tu misión es ejecutar una auditoría técnica y un análisis de confluencia normativa sobre sistemas de IA desplegados en INFRAESTRUCTURA CRÍTICA.

Evalúa el documento proporcionado considerando la convergencia de estos tres marcos:
1. ISO 27001: Seguridad de la información base (Controles de acceso, logs, vulnerabilidades).
2. NIST AI RMF: Gestión de riesgos específicos de IA (Gobernanza, Robustez Adversarial, Explicabilidad).
3. ISO 42001: Sistema de Gestión de IA (Responsabilidad, transparencia, supervisión humana).

Criterios de evaluación:
1. EXISTENCIA: ¿El control o requisito está presente?
2. RIGOR EN INFRAESTRUCTURA CRÍTICA: ¿El control es suficiente para sectores de alto riesgo (Finanzas, Salud, Energía)?
3. CONFLUENCIA: ¿El documento articula los requisitos de ciberseguridad con los de IA confiable?

Estados:
- ✅ CONFORME: Cumple los requisitos de los tres marcos con rigor.
- ⚠️ PARCIAL: Falta alineación con alguno de los marcos o falta rigor para infraestructura crítica.
- ❌ NO CONFORME: El control no existe o es crítico en sistemas de alto riesgo.

INSTRUCCIONES DE FORMATO:
- Responde ÚNICAMENTE con una tabla Markdown con exactamente 4 columnas:
  | Control / Requisito (Marco Confluente) | Estado | Observación Técnica (Infraestructura Crítica) | Acción de Mejora |
- Al final, agrega un RESUMEN EJECUTIVO de confluencia."""

    # RAG: Extraer contexto de la norma oficial
    contexto_oficial = ""
    rag_funciona = False
    if usar_rag:
        try:
            from rag_knowledge import base_conocimiento_activa, obtener_contexto
            if base_conocimiento_activa():
                contexto_oficial = obtener_contexto(texto_politica[:1500], k=4, incluir_uploads=True)
                rag_funciona = bool(contexto_oficial)
            else:
                contexto_oficial = ""
                rag_funciona = False
        except Exception:
            contexto_oficial = ""
            rag_funciona = False

    if contexto_oficial:
        contexto_oficial_texto = f"\n\n--- INICIO CONTEXTO NORMA OFICIAL (RAG) ---\n{contexto_oficial}\n--- FIN CONTEXTO ---\nUtiliza este contexto para evaluar la política."
    else:
        if usar_rag and not rag_funciona:
            contexto_oficial_texto = "\n\nNota: Base de conocimiento RAG no disponible. Análisis realizado con conocimiento general del LLM."
        else:
            contexto_oficial_texto = "\n\nNota: Análisis realizado sin base de conocimiento RAG (deshabilitado por configuración)."

    user_prompt = f"""Ejecuta el Gap Analysis sobre el siguiente documento de política de seguridad:

---INICIO DEL DOCUMENTO DE POLÍTICA---
{texto_politica}
---FIN DEL DOCUMENTO DE POLÍTICA---{contexto_oficial_texto}

Genera la tabla de Gap Analysis ISO/IEC 27001:2022 completa."""

    mensajes = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    respuesta = llm.invoke(mensajes)
    return respuesta.content


def ejecutar_chat(mensajes_historial: list, proveedor: str, modelo_llm: str, temp: float):
    try:
        llm = _construir_llm(proveedor, modelo_llm, temp)
    except ValueError as e:
        return f"⚠️ Error de configuración: {e}"

    system_prompt = SystemMessage(content="Eres un Auditor experto en ISO 27001, NIST y ISO 42001. Responde de forma profesional y técnica.")
    formatted_messages = [system_prompt]
    for m in mensajes_historial:
        if m["role"] == "user":
            formatted_messages.append(HumanMessage(content=m["content"]))
        else:
            formatted_messages.append(AIMessage(content=m["content"]))
    try:
        respuesta = llm.invoke(formatted_messages)
        return respuesta.content
    except Exception as e:
        return f"⚠️ El asistente no pudo responder: {e}"
