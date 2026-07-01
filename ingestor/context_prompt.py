CUESTIONARIO_CONTEXTO = [
    {
        "id": "pais",
        "pregunta": "¿En qué país opera principalmente la organización?",
        "tipo": "select",
        "opciones": [
            "Colombia",
            "Latinoamérica (otro país)",
            "Estados Unidos / Canadá",
            "Europa",
            "Otro",
        ],
        "obligatorio": True,
    },
    {
        "id": "sector",
        "pregunta": "¿Cuál es el sector principal de la organización?",
        "tipo": "select",
        "opciones": [
            "Energía y Utilities", "Salud y Ciencias de la Vida",
            "Servicios Financieros", "Transporte y Logística",
            "Gobierno y Defensa", "Telecomunicaciones",
            "Agua y Saneamiento", "Tecnología / Software",
            "Educación", "Otro sector",
        ],
        "obligatorio": True,
    },
    {
        "id": "tamano",
        "pregunta": "¿Cuál es el tamaño aproximado de la organización?",
        "tipo": "select",
        "opciones": [
            "Pequeña (1-50 empleados)", "Mediana (51-500 empleados)",
            "Grande (501-5000 empleados)", "Corporación (>5000 empleados)",
        ],
        "obligatorio": True,
    },
    {
        "id": "sistemas_ia",
        "pregunta": "¿Qué sistemas de IA tiene actualmente en producción?",
        "tipo": "multiselect",
        "opciones": [
            "Chatbots / Asistentes virtuales (LLM)",
            "Visión por computadora / Reconocimiento de imágenes",
            "Modelos predictivos (riesgo, demanda, fraude)",
            "Sistemas de recomendación",
            "Automatización de procesos (RPA + IA)",
            "Procesamiento de lenguaje natural (NLP)",
            "Vehículos autónomos / Robótica",
            "Sistemas de toma de decisiones automatizadas",
            "Ninguno / En fase de exploración",
        ],
        "obligatorio": True,
    },
    {
        "id": "normas_aplica",
        "pregunta": "¿Qué marcos normativos le aplican actualmente?",
        "tipo": "multiselect",
        "opciones": [
            "ISO/IEC 27001:2022 (Seguridad de la información)",
            "ISO/IEC 42001:2023 (Sistema de Gestión de IA)",
            "NIST AI RMF 1.0",
            "ISO/IEC 23894:2023 (Gestión de riesgos de IA)",
            "ISO 31000:2018 (Gestión de riesgos)",
            "PCI DSS v4.0",
            "HIPAA / FDA (Salud)",
            "SOX / Basel (Financiero)",
            "NERC CIP (Energía)",
            "Ninguno / En proceso de adopción",
        ],
        "obligatorio": False,
    },
    {
        "id": "exposicion",
        "pregunta": "¿Cuál es el nivel de exposición de sus sistemas de IA al público/externos?",
        "tipo": "select",
        "opciones": [
            "Alto: APIs públicas, chatbots面向 clientes externos",
            "Medio: Sistemas internos con acceso desde redes externas",
            "Bajo: Sistemas aislados en red interna sin acceso externo",
            "Muy Bajo: Sistemas sin conexión de red (air-gapped)",
        ],
        "obligatorio": True,
    },
    {
        "id": "incidentes_previos",
        "pregunta": "¿Ha tenido incidentes de seguridad relacionados con IA en los últimos 12 meses?",
        "tipo": "select",
        "opciones": [
            "Sí, múltiples incidentes",
            "Sí, al menos un incidente",
            "No, pero tenemos conocimiento de intentos",
            "No, sin incidentes conocidos",
            "No sabemos / No tenemos visibilidad",
        ],
        "obligatorio": True,
    },
    {
        "id": "madurez_gobierno",
        "pregunta": "¿Cuál es el nivel de madurez de su gobierno de IA?",
        "tipo": "select",
        "opciones": [
            "Inexistente: Sin políticas ni procesos de IA",
            "Inicial: Políticas informales, sin estandarización",
            "Definido: Políticas documentadas y procesos establecidos",
            "Gestionado: Monitoreo y métricas de IA implementados",
            "Optimizado: Mejora continua y automatización",
        ],
        "obligatorio": True,
    },
    {
        "id": "datos_sensibles",
        "pregunta": "¿Sus sistemas de IA procesan datos sensibles o críticos?",
        "tipo": "multiselect",
        "opciones": [
            "Datos personales / Privacidad (GDPR, Ley 1581)",
            "Datos biométricos / Genómicos",
            "Datos financieros / Transaccionales",
            "Datos de infraestructura crítica",
            "Datos clasificados / Seguridad nacional",
            "Secretos industriales / Propiedad intelectual",
            "No procesamos datos sensibles",
        ],
        "obligatorio": True,
    },
    {
        "id": "proveedores_ia",
        "pregunta": "¿Utiliza modelos o servicios de IA de terceros (proveedores externos)?",
        "tipo": "select",
        "opciones": [
            "Sí, modelos comerciales (OpenAI, Anthropic, Google, etc.)",
            "Sí, modelos open source (Llama, Mistral, etc.) desplegados por nosotros",
            "Sí, combinación de modelos propios y de terceros",
            "No, todos los modelos son desarrollados internamente",
            "No aplica / No usamos IA",
        ],
        "obligatorio": True,
    },
    {
        "id": "objetivo_privacidad",
        "pregunta": "¿Cuál es su objetivo principal con la Matriz de Riesgos de IA?",
        "tipo": "select",
        "opciones": [
            "Cumplimiento regulatorio (ISO 42001, NIST AI RMF)",
            "Gestión de riesgos operativos de IA",
            "Preparación para auditoría externa",
            "Mejora de seguridad en sistemas de IA existentes",
            "Debida diligencia antes de implementar nuevos sistemas de IA",
            "Conciencia organizacional sobre riesgos de IA",
        ],
        "obligatorio": True,
    },
]


def generar_prompt_contexto(respuestas: dict) -> str:
    """
    Genera un prompt estructurado para DeepSeek basado en las respuestas
    del cuestionario contextual, para personalizar la matriz de riesgos.
    """
    sector = respuestas.get("sector", "No especificado")
    tamano = respuestas.get("tamano", "No especificado")
    sistemas = respuestas.get("sistemas_ia", [])
    normas = respuestas.get("normas_aplica", [])
    exposicion = respuestas.get("exposicion", "No especificada")
    incidentes = respuestas.get("incidentes_previos", "No especificado")
    madurez = respuestas.get("madurez_gobierno", "No especificada")
    datos = respuestas.get("datos_sensibles", [])
    proveedores = respuestas.get("proveedores_ia", "No especificado")
    objetivo = respuestas.get("objetivo_privacidad", "No especificado")
    pais = respuestas.get("pais", "No especificado")

    # Normativa colombiana adicional según el país
    normativa_pais = ""
    if "Colombia" in pais:
        normativa_pais = """
### Normativa colombiana aplicable (por país)
- Ley 1581 de 2012 - Protección de Datos Personales
- Decreto 1377 de 2013 - Reglamentación Ley 1581
- Ley 1266 de 2008 - Habeas Data Financiero
- CONPES 3995 de 2020 - Política Nacional de Ciberseguridad
- CONPES 4069 de 2022 - Política Nacional de Inteligencia Artificial
- Proyecto Ley 059 de 2023 - Regulación de IA en Colombia (en trámite)
- Circular 007 de 2018 - Superintendencia Financiera
- Resolución MinTIC 20223040026965 de 2022
- Ley 2195 de 2022 - Transparencia en IA del Estado
- Decreto 620 de 2020 - Confianza digital
- NTC-ISO 27001 - Norma Técnica Colombiana"""

    prompt = f"""## CONTEXTO ORGANIZACIONAL PARA MATRIZ DE RIESGOS DE IA

### Datos de la organización
- **País:** {pais}
- **Sector:** {sector}
- **Tamaño:** {tamano}
- **Sistemas de IA en producción:** {', '.join(sistemas) if isinstance(sistemas, list) else sistemas}
- **Exposición de sistemas IA:** {exposicion}
- **Incidentes previos (12 meses):** {incidentes}
- **Madurez de gobierno IA:** {madurez}
- **Datos sensibles procesados:** {', '.join(datos) if isinstance(datos, list) else datos}
- **Proveedores de IA externos:** {proveedores}
- **Objetivo principal:** {objetivo}

### Marcos normativos aplicables
{chr(10).join('- ' + n for n in normas) if isinstance(normas, list) else normas}
{normativa_pais}
### Perfil de riesgo inferido
- **Factor de exposición:** {'CRÍTICO' if 'Alto' in exposicion or 'API' in exposicion else 'MODERADO' if 'Medio' in exposicion else 'BAJO'}
- **Factor de madurez:** {'CRÍTICO' if 'Inexistente' in madurez or 'Inicial' in madurez else 'MODERADO' if 'Definido' in madurez else 'GESTIONADO'}
- **Factor de incidentes:** {'CRÍTICO' if 'múltiples' in incidentes else 'MODERADO' if 'incidente' in incidentes else 'BAJO'}
- **Factor de datos sensibles:** {'CRÍTICO' if any(d in ('Datos biométricos / Genómicos', 'Datos clasificados', 'Datos de infraestructura crítica') for d in (datos if isinstance(datos, list) else [])) else 'MODERADO'}
- **Factor país:** {'CRÍTICO' if 'Colombia' in pais else 'MODERADO' if 'Latinoamérica' in pais or 'Europa' in pais else 'BAJO'}
"""
    return prompt
