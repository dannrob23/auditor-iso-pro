import json
import os
import time
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

DEFAULT_PROVIDER = os.getenv("NORMALIZER_PROVIDER", "deepseek")
MODEL_MAP = {
    "google": ["gemini-2.5-pro", "gemini-2.5-flash"],
    "deepseek": ["deepseek-chat", "deepseek-coder"],
}

SYSTEM_PROMPT = """Eres un Arquitecto de Riesgos de IA que explica vulnerabilidades a personas que NO hablan inglés.
Analiza el reporte en inglés y TRADÚCELO TODO al español con lenguaje SENCILLO y CLARO.
REGLA ESTRICTA: Tu respuesta debe ser ÚNICAMENTE un objeto JSON válido, sin markdown ni explicaciones adicionales.
Campos obligatorios y su significado:
{
    "id_vulnerabilidad": "ID único de la fuente (ej. AVID-2026-R12)",
    "fuente_origen": "Indicar si es AVID, MITRE ATLAS, MIT AI Risk o NVD",
    "descripcion_riesgo": "EXPLICACIÓN EN ESPAÑOL SENCILLO: ¿Por qué es un riesgo para la organización? ¿Qué impacto puede tener en el negocio? (máximo 3 líneas)",
    "resumen_es": "RESUMEN EN ESPAÑOL: ¿Qué hace esta vulnerabilidad? Explica como si fuera para una persona sin conocimientos técnicos (máximo 4 líneas)",
    "causa_raiz": "CAUSA EN ESPAÑOL: ¿Cuál es el origen del problema? ¿Qué falla técnicamente? Explícalo simple",
    "accion_remediacion": "SOLUCIÓN EN ESPAÑOL: ¿Cómo se previene o se soluciona? Pasos claros y prácticos",
    "tactica_mitre": "Táctica MITRE ATLAS aplicable (ej. AML.T0051 - Inyección de Prompts)",
    "clasificacion_tipo": "Tipo: Adversarial, Privacidad, Sesgo, Seguridad Fisica, Datos, Societal, o Tecnico",
    "normas_aplicables": ["ISO 27001 A.8.8 - Gestión de vulnerabilidades técnicas", "NIST AI RMF 3.0", "ISO 42001 A.7.3 - Seguridad en IA", "ISO 23894 5.5 - Robusteza adversarial"],
    "probabilidad_base": 3,
    "severidad_tecnica": 4,
    "controles_nist": "Control técnico recomendado en NIST AI RMF (explicado en español)",
    "como_se_ejecuta": "EXPLICACIÓN EN ESPAÑOL: ¿Cómo ejecuta un atacante esta vulnerabilidad? Pasos simples",
    "como_prevenirlo": "EXPLICACIÓN EN ESPAÑOL: ¿Qué medidas prácticas tomar para evitar este riesgo?"
}
IMPORTANTE: resumen_es, causa_raiz, accion_remediacion, como_se_ejecuta, como_prevenirlo, descripcion_riesgo y controles_nist deben estar 100% en español.
Usa vocabulario simple, evita tecnicismos innecesarios. Piensa que lo lee un gerente o auditor no técnico."""


_PROVIDER: str | None = None
_MODEL_NAME: str | None = None


def set_provider(provider: str, model: str = ""):
    """
    Configura el proveedor y modelo para la normalización.
    provider: "google", "deepseek"
    """
    global _PROVIDER, _MODEL_NAME
    _PROVIDER = provider
    models = MODEL_MAP.get(provider, [])
    _MODEL_NAME = model if model in models else (models[0] if models else "deepseek-chat")


def _get_provider() -> str:
    return _PROVIDER or DEFAULT_PROVIDER


def _get_model() -> str:
    return _MODEL_NAME or MODEL_MAP.get(_get_provider(), ["deepseek-chat"])[0]


def _call_llm(user_prompt: str, system_prompt: str, max_retries: int = 2) -> Optional[str]:
    """
    Llama al LLM configurado (Google Gemini o DeepSeek) y retorna el texto de respuesta.
    """
    provider = _get_provider()
    model = _get_model()

    for attempt in range(max_retries):
        try:
            if provider == "google":
                from google import genai
                api_key = GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY", "")
                if not api_key:
                    print("[Normalizer] GOOGLE_API_KEY no configurada.")
                    return None
                client = genai.Client(api_key=api_key)
                resp = client.models.generate_content(
                    model=model,
                    contents=f"{system_prompt}\n\n{user_prompt}",
                    config={"temperature": 0.1, "max_output_tokens": 1024},
                )
                text = resp.text
                # Limpiar markdown wrapper
                if "```" in text:
                    text = text.split("```")[-2] if text.count("```") >= 2 else text
                    text = text.split("\n", 1)[-1] if "\n" in text else text
                return text.strip()
            else:
                if not DEEPSEEK_API_KEY and not os.getenv("DEEPSEEK_API_KEY"):
                    print("[Normalizer] DEEPSEEK_API_KEY no configurada.")
                    return None
                key = DEEPSEEK_API_KEY or os.getenv("DEEPSEEK_API_KEY", "")
                client = OpenAI(api_key=key, base_url="https://api.deepseek.com/v1")
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.1,
                    max_tokens=1024,
                )
                return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Normalizer] Intento {attempt + 1}/{max_retries} ({provider}/{model}) falló: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            continue
    return None


def analizar_vulnerabilidad(fuente: str, texto_reporte: dict | str, max_retries: int = 2) -> dict:
    """
    Envía un reporte de vulnerabilidad al LLM configurado (Google Gemini o DeepSeek) para normalización.
    Retorna el JSON parseado o el resultado del normalizador local.
    """
    if isinstance(texto_reporte, dict):
        cleaned = {}
        for k, v in texto_reporte.items():
            if hasattr(v, 'isoformat'):
                cleaned[k] = v.isoformat()
            elif isinstance(v, list):
                cleaned[k] = [str(i) if hasattr(i, 'isoformat') else i for i in v]
            else:
                cleaned[k] = v
        report_text = json.dumps(cleaned, ensure_ascii=False)
    else:
        report_text = str(texto_reporte)

    user_prompt = (
        f"Fuente: {fuente}\n"
        f"Reporte de vulnerabilidad:\n{report_text}\n\n"
        "Normaliza este reporte siguiendo el esquema JSON especificado. "
        "Pon especial atención en asignar probabilidad_base (1-5), severidad_tecnica (1-5), "
        "y la lista de normas_aplicables concretas."
    )

    for attempt in range(max_retries):
        try:
            content = _call_llm(user_prompt, SYSTEM_PROMPT, max_retries=1)
            if not content:
                continue
            content = content.strip()

            if "```" in content:
                content = content.split("```")[-2] if content.count("```") >= 2 else content
                if "\n" in content:
                    content = content.split("\n", 1)[-1] if content.startswith("```") else content

            # Intentar extraer JSON directamente si hay texto antes/después
            if content.startswith("{"):
                parsed = json.loads(content)
            else:
                import re as _re
                json_match = _re.search(r'\{.*\}', content, _re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                else:
                    raise json.JSONDecodeError("No JSON found in response", content, 0)
            if "probabilidad_base" not in parsed:
                parsed["probabilidad_base"] = 3
            if "severidad_tecnica" not in parsed:
                parsed["severidad_tecnica"] = 3
            if "normas_aplicables" not in parsed:
                parsed["normas_aplicables"] = []
            if "resumen_es" not in parsed:
                parsed["resumen_es"] = parsed.get("descripcion_riesgo", "Sin resumen")
            if "causa_raiz" not in parsed:
                parsed["causa_raiz"] = "No especificada"
            if "accion_remediacion" not in parsed:
                parsed["accion_remediacion"] = "No especificada"
            if "clasificacion_tipo" not in parsed:
                parsed["clasificacion_tipo"] = "Tecnico"
            parsed["fuente_origen"] = fuente
            clasif = parsed.get("clasificacion_tipo", "Tecnico")
            parsed["normativa_colombia"] = NORMATIVA_COLOMBIA.get(clasif, NORMATIVA_COLOMBIA["Tecnico"])
            return parsed

        except (json.JSONDecodeError, Exception) as e:
            print(f"[Normalizer] Intento {attempt + 1}/{max_retries} falló: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            continue

    return _normalize_local(fuente, texto_reporte)


def _normalize_local(fuente: str, texto_reporte: dict | str) -> dict:
    """Fallback local cuando DeepSeek no está disponible."""
    if isinstance(texto_reporte, dict):
        title = texto_reporte.get("title", texto_reporte.get("name", "Sin título"))
        desc = texto_reporte.get("description", texto_reporte.get("descripcion_riesgo", "Sin descripción"))
        sev = texto_reporte.get("severity", 3)
        prob = texto_reporte.get("likelihood", texto_reporte.get("probabilidad_base", 3))
        vid = texto_reporte.get("id", "PENDIENTE")
        remed = texto_reporte.get("remediation", texto_reporte.get("accion_remediacion", "Consulta con el equipo de seguridad"))
        tactica = texto_reporte.get("classification", texto_reporte.get("mitre_tactic", texto_reporte.get("tactica_mitre", "AML.PENDIENTE")))
        nist_ctrl = texto_reporte.get("nist_controls", [])
        if isinstance(nist_ctrl, list):
            nist_ctrl = "; ".join(nist_ctrl)
        affected = texto_reporte.get("affected_systems", [])
    else:
        title = "Reporte sin estructurar"
        desc = str(texto_reporte)[:200]
        sev = 3
        prob = 3
        vid = "PENDIENTE"
        remed = "Analizar manualmente"
        tactica = "AML.PENDIENTE"
        nist_ctrl = "NIST AI RMF"
        affected = []

    # Clasificación mejorada según fuente y contenido
    clasificacion = _clasificar_por_tactica(tactica)
    if clasificacion == "Tecnico" and fuente == "MITRE ATLAS":
        # MITRE ATLAS techniques son todas adversariales
        clasificacion = "Adversarial"
    elif clasificacion == "Tecnico" and fuente == "AVID":
        # Inferir clasificación desde el título AVID
        t_lower = title.lower()
        if any(w in t_lower for w in ["bias", "fairness", "gender", "discriminat"]):
            clasificacion = "Sesgo"
        elif any(w in t_lower for w in ["privacy", "leak", "data", "pii", "inference"]):
            clasificacion = "Privacidad"
        elif any(w in t_lower for w in ["adversar", "evasion", "bypass", "backdoor", "poison"]):
            clasificacion = "Adversarial"
        elif any(w in t_lower for w in ["safety", "crash", "kill", "injure", "malfunction"]):
            clasificacion = "Seguridad Fisica"
        elif any(w in t_lower for w in ["deepfake", "misinform", "disinform"]):
            clasificacion = "Societal"
    elif clasificacion == "Tecnico" and fuente == "MIT AI Risk Repository":
        clasificacion = _clasificar_mit_domain(tactica)

    normas = _normas_por_tactica(tactica)
    if fuente == "AVID":
        normas = list(set(normas + ["AVID Taxonomy v0.1", "ISO 23894:2023"]))
    elif fuente == "MIT AI Risk Repository":
        normas = list(set(normas + ["MIT AI Risk Taxonomy", "arXiv:2408.12622"]))

    # Generar explicaciones en español para modo local
    expl_causa, expl_ejecuta, expl_previene = _generar_explicaciones_es(clasificacion, title, tactica)

    return {
        "id_vulnerabilidad": vid,
        "fuente_origen": fuente,
        "descripcion_riesgo": _resumen_impacto_es(clasificacion, title),
        "resumen_es": title,
        "causa_raiz": expl_causa,
        "accion_remediacion": f"{remed[:150]}. {expl_previene}",
        "tactica_mitre": tactica,
        "clasificacion_tipo": clasificacion,
        "normas_aplicables": normas,
        "normativa_colombia": NORMATIVA_COLOMBIA.get(clasificacion, NORMATIVA_COLOMBIA["Tecnico"]),
        "probabilidad_base": prob if 1 <= prob <= 5 else 3,
        "severidad_tecnica": sev if 1 <= sev <= 5 else 3,
        "controles_nist": nist_ctrl,
        "sistemas_afectados": affected,
        "como_se_ejecuta": expl_ejecuta,
        "como_prevenirlo": expl_previene,
    }


MITRE_DOMAIN_MAP = {
    "Discrimination & Toxicity": "Sesgo",
    "Privacy & Security": "Privacidad",
    "Misinformation": "Societal",
    "Malicious Actors": "Adversarial",
    "Human-Computer Interaction": "Tecnico",
    "Socioeconomic & Environmental": "Societal",
    "AI System Safety, Failures, & Limitations": "Seguridad Fisica",
}


def _clasificar_mit_domain(domain: str) -> str:
    for key, value in MITRE_DOMAIN_MAP.items():
        if key.lower() in domain.lower():
            return value
    return "Tecnico"


def _clasificar_por_tactica(tactica: str) -> str:
    t = tactica.upper()
    if "INJECTION" in t or "ADVERSARIAL" in t or "PATCH" in t or "EVASION" in t or "BYPASS" in t:
        return "Adversarial"
    if "INVERSION" in t or "PRIVACY" in t or "PRIVACIDAD" in t or "EXFILTRATION" in t or "STEAL" in t:
        return "Privacidad"
    if "BIAS" in t or "SESGO" in t or "FAIRNESS" in t or "DISCRIMINAT" in t or "ETHICS" in t:
        return "Sesgo"
    if "SAFETY" in t or "FISICA" in t or "PHYSICAL" in t or "AUTONOM" in t or "WEAPON" in t or "CRASH" in t or "KILL" in t:
        return "Seguridad Fisica"
    if "POISON" in t or "DATA" in t or "DATO" in t or "SUPPLY CHAIN" in t:
        return "Datos"
    if "DISINFORMATION" in t or "SOCIETAL" in t or "SOCI" in t or "SURVEILLANCE" in t or "MISINFORM" in t or "DEEPFAKE" in t:
        return "Societal"
    if "RECONNAISSANCE" in t or "DISCOVERY" in t or "COLLECTION" in t:
        return "Tecnico"
    if "PERSISTENCE" in t or "DEFENSE" in t or "EXECUTION" in t or "IMPACT" in t:
        return "Adversarial"
    return "Tecnico"


# ── Normativa colombiana aplicable por tipo de vulnerabilidad ──────────────
NORMATIVA_COLOMBIA = {
    "Adversarial": [
        "Ley 1581/2012 - Protección de Datos (principio de seguridad)",
        "Circular 007/2018 SFC - Gestión riesgos ciberseguridad financiera",
        "CONPES 3995/2020 - Política Nacional de Ciberseguridad",
        "Resolución MinTIC 20223040026965/2022 - Ciberseguridad entidades públicas",
    ],
    "Privacidad": [
        "Ley 1581/2012 - Protección de Datos Personales (Art. 4, 10, 17)",
        "Decreto 1377/2013 - Reglamentación Ley 1581",
        "Ley 1266/2008 - Habeas Data Financiero",
        "CONPES 4069/2022 Eje 2 - Política Nacional de IA",
    ],
    "Sesgo": [
        "Ley 1581/2012 Art. 4 - Principio de no discriminación",
        "CONPES 4069/2022 Eje 2 - Marco ético para IA",
        "Proyecto Ley 059/2023 - Regulación de IA en Colombia",
        "Decreto 1081/2015 - Transparencia y acceso a información pública",
    ],
    "Seguridad Fisica": [
        "CONPES 3995/2020 - Infraestructura Crítica (salud, energía, finanzas, gobierno)",
        "Resolución MinTIC 20223040026965/2022",
        "Ley 2195/2022 - Transparencia en IA del Estado",
        "CONPES 4069/2022 Eje 4 - Seguridad en IA",
    ],
    "Datos": [
        "Ley 1581/2012 - Políticas de tratamiento de datos",
        "Decreto 1377/2013 Art. 11 - Autorización del titular",
        "Decreto 1074/2015 - Integridad de la información",
        "CONPES 4069/2022 - Gobernanza de datos para IA",
    ],
    "Societal": [
        "CONPES 4069/2022 - Impacto social de IA",
        "Proyecto Ley 059/2023 - Transparencia algorítmica",
        "Ley 2195/2022 - Rendición de cuentas en IA pública",
        "Ley 1712/2014 - Transparencia y acceso a información",
    ],
    "Tecnico": [
        "Resolución MinTIC 20223040026965/2022 - Seguridad infraestructura TI",
        "CONPES 3995/2020 - Ciberseguridad nacional",
        "Decreto 620/2020 - Política de confianza digital",
        "Norma Técnica Colombiana NTC-ISO 27001",
    ],
}


def _normas_por_tactica(tactica: str, pais: str = "COLOMBIA") -> list[str]:
    t = tactica.upper()
    base = ["ISO 27001:2022 A.8.8 - Gestión de vulnerabilidades"]

    if "INJECTION" in t:
        base += ["NIST AI RMF 3.0 - Robustness Testing", "ISO 42001:2023 A.7.3", "OWASP LLM Top 10"]
    elif "BIAS" in t or "FAIRNESS" in t or "DISCRIMINAT" in t or "ETHICS" in t:
        base += ["NIST AI RMF 2.6 - Fairness", "ISO 42001:2023 A.6.2", "ISO 23894:2023 5.3"]
    elif "PRIVACY" in t or "INVERSION" in t or "INFERENCE" in t:
        base += ["NIST AI RMF 2.0 - Privacy", "ISO 27001:2022 A.8.12", "GDPR Art. 22"]
    elif "SAFETY" in t or "AUTONOM" in t or "PHYSICAL" in t:
        base += ["NIST AI RMF 3.0 - Safety", "ISO 23894:2023 5.5", "IEC 62443"]
    elif "POISON" in t or "SUPPLY CHAIN" in t:
        base += ["NIST AI RMF 2.0 - Data Integrity", "ISO 27001:2022 A.8.10", "ISO 42001:2023 A.7.1"]
    elif "DISINFORMATION" in t or "SOCIETAL" in t or "DEEPFAKE" in t:
        base += ["NIST AI RMF 2.0 - Transparency", "ISO 42001:2023 A.6.1", "C2PA Standards"]
    else:
        base += ["NIST AI RMF 3.0", "ISO 42001:2023 A.7.3", "ISO 23894:2023 5.5"]

    # Agregar normativa colombiana según clasificación
    clasificacion = _clasificar_por_tactica(tactica)
    col_norms = NORMATIVA_COLOMBIA.get(clasificacion, NORMATIVA_COLOMBIA["Tecnico"])
    base += col_norms

    return base


def normalize_batch(reportes: list[dict], fuente: str | None = None) -> list[dict]:
    """
    Normaliza un lote de reportes de una misma fuente.
    """
    resultados = []
    for reporte in reportes:
        f = fuente or reporte.get("source", "DESCONOCIDA")
        resultado = analizar_vulnerabilidad(f, reporte)
        resultados.append(resultado)
    return resultados


def _resumen_impacto_es(clasificacion: str, titulo: str) -> str:
    """Genera un resumen de impacto en español según la clasificación."""
    impactos = {
        "Adversarial": "Un atacante puede manipular el sistema de IA para que tome decisiones incorrectas o maliciosas, afectando la seguridad y confiabilidad del sistema.",
        "Privacidad": "El sistema de IA puede exponer información privada de personas, como datos personales, médicos o financieros, violando la privacidad.",
        "Sesgo": "El sistema de IA puede discriminar a ciertos grupos de personas, dando resultados injustos por razones de género, raza u otras características.",
        "Seguridad Fisica": "El sistema de IA puede causar daños físicos a personas, equipos o infraestructura si falla o es manipulado.",
        "Datos": "Los datos usados para entrenar el sistema de IA pueden estar contaminados o ser robados, afectando su precisión y confiabilidad.",
        "Societal": "El uso del sistema de IA puede tener impactos negativos en la sociedad, como desinformación, vigilancia masiva o desigualdad.",
        "Tecnico": "El sistema de IA tiene una debilidad técnica que puede ser aprovechada por un atacante para comprometer su funcionamiento.",
    }
    base = impactos.get(clasificacion, "Esta vulnerabilidad representa un riesgo para el sistema de IA.")
    return f"{base} Vulnerabilidad: {titulo[:100]}."


def _generar_explicaciones_es(clasificacion: str, titulo: str, tactica: str) -> tuple[str, str, str]:
    """
    Genera causa_raiz, como_se_ejecuta, como_prevenirlo en español
    según la clasificación de la vulnerabilidad.
    """
    explicaciones = {
        "Adversarial": (
            "La causa raíz es que el sistema de IA no fue diseñado para resistir entradas maliciosas. "
            "Los modelos de IA pueden ser engañados con datos especialmente modificados.",
            "El atacante envía datos modificados especialmente (por ejemplo, una imagen con un pequeño cambio invisible "
            "para el ojo humano, o un texto con instrucciones ocultas). El sistema de IA procesa estos datos "
            "y da una respuesta equivocada: no detecta un peligro, clasifica algo incorrectamente o revela información sensible.",
            "Usar técnicas de entrenamiento adversarial (enseñar al modelo a resistir ataques), "
            "validar todas las entradas antes de procesarlas, implementar supervisión humana en decisiones críticas, "
            "y realizar pruebas periódicas de seguridad con equipos especializados."
        ),
        "Privacidad": (
            "Los modelos de IA pueden memorizar y reproducir datos sensibles con los que fueron entrenados, "
            "o un atacante puede hacer consultas diseñadas para extraer información privada.",
            "El atacante hace muchas consultas al sistema de IA con preguntas cuidadosamente diseñadas. "
            "Analizando las respuestas, puede reconstruir datos personales de los usuarios que se usaron "
            "para entrenar el modelo, como nombres, direcciones, historiales médicos o financieros.",
            "Usar privacidad diferencial durante el entrenamiento (técnica que añade ruido para ocultar datos individuales), "
            "limitar cuántas respuestas puede dar el sistema, filtrar información sensible en las salidas, "
            "y cifrar los datos de entrenamiento."
        ),
        "Sesgo": (
            "El sistema de IA fue entrenado con datos que no representan adecuadamente a todos los grupos de personas, "
            "o los datos históricos contienen sesgos existentes en la sociedad.",
            "El sistema aprende patrones de los datos de entrenamiento. Si esos datos tienen sobre-representación de ciertos grupos "
            "o contienen decisiones humanas sesgadas, el sistema reproduce y amplifica esos sesgos. "
            "Por ejemplo, un sistema de contratación entrenado con datos históricos puede aprender a discriminar a mujeres "
            "porque en el pasado contrataron más hombres.",
            "Auditar los datos de entrenamiento para detectar sesgos, usar conjuntos de datos balanceados, "
            "implementar métricas de equidad que monitoreen el desempeño del sistema por grupos poblacionales, "
            "y realizar auditorías periódicas de sesgo con equipos diversos."
        ),
        "Seguridad Fisica": (
            "El sistema de IA controla dispositivos físicos (vehículos, robots, maquinaria) pero no tiene "
            "suficientes mecanismos de seguridad para prevenir fallos catastróficos.",
            "Un atacante puede manipular los sensores del dispositivo (cámaras, LIDAR, sensores de proximidad) "
            "para que el sistema de IA perciba incorrectamente su entorno. "
            "Por ejemplo, poner una pegatina en una señal de stop para que un vehículo autónomo la lea como límite de velocidad. "
            "O el sistema puede fallar por sí solo si encuentra una situación para la que no fue entrenado.",
            "Implementar múltiples sensores redundantes (que un fallo en uno no afecte al sistema), "
            "tener mecanismos de parada de emergencia manual, validar físicamente las decisiones del sistema antes de ejecutarlas, "
            "y realizar pruebas exhaustivas en entornos controlados antes del despliegue."
        ),
        "Datos": (
            "Los datos utilizados para entrenar o alimentar el sistema de IA pueden ser manipulados por un atacante "
            "antes de que el sistema los procese.",
            "El atacante introduce datos falsos o modificados en el conjunto de entrenamiento del sistema de IA. "
            "Por ejemplo, si un banco usa IA para detectar fraudes, el atacante puede 'envenenar' los datos de entrenamiento "
            "para que el sistema aprenda a no detectar cierto tipo de transacciones fraudulentas. "
            "O puede inyectar datos maliciosos en la cadena de suministro del modelo.",
            "Verificar la procedencia de todos los datos de entrenamiento, implementar detección de anomalías en los datos, "
            "usar técnicas de entrenamiento robustas que limiten el impacto de datos maliciosos, "
            "y mantener un inventario actualizado de todas las fuentes de datos."
        ),
        "Societal": (
            "El uso del sistema de IA puede tener consecuencias negativas para la sociedad en general, "
            "como desinformación masiva, vigilancia no consentida o manipulación de la opinión pública.",
            "El atacante utiliza sistemas de IA generativa (como modelos de lenguaje o generación de imágenes) "
            "para crear contenido falso pero convincente a gran escala: noticias falsas, videos deepfake, "
            "reseñas fraudulentas, o campañas de manipulación en redes sociales. "
            "La IA permite automatizar y escalar estas operaciones a un nivel imposible para humanos.",
            "Implementar sistemas de detección de contenido generado por IA, usar estándares de procedencia "
            "de contenido (C2PA), educar al público sobre cómo identificar desinformación, "
            "y establecer marcos regulatorios que exijan transparencia en el uso de IA generativa."
        ),
        "Tecnico": (
            "El sistema de IA tiene debilidades en su infraestructura técnica que pueden ser explotadas: "
            "falta de controles de acceso, configuraciones inseguras, o dependencias de software vulnerable.",
            "El atacante explora la infraestructura del sistema de IA buscando puertas abiertas: "
            "APIs sin autenticación, repositorios de modelos públicos, configuraciones por defecto, "
            "o dependencias de software con vulnerabilidades conocidas. "
            "Una vez dentro, puede robar el modelo, modificarlo o usarlo como puerta de entrada a otros sistemas.",
            "Implementar controles de acceso estrictos, mantener el software actualizado, "
            "realizar análisis de vulnerabilidades periódicos, usar contenedores seguros para modelos, "
            "y seguir las guías de seguridad de OWASP para sistemas de IA."
        ),
    }

    return explicaciones.get(clasificacion, (
        f"Causa técnica documentada en la fuente como: {tactica}",
        "Consultar la documentación técnica de la fuente para detalles específicos de ejecución.",
        "Aplicar los controles recomendados por NIST AI RMF, ISO 27001 e ISO 42001 según corresponda."
    ))
