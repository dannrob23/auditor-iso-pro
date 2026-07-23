"""
Módulo de Autodiagnóstico IA-SEC
Evalúa la madurez del modelo de IA mediante un cuestionario estructurado
y genera automáticamente una propuesta de implementación basada en ISO 19011.
"""
import json
import os
import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
# DIMENSIONES Y PREGUNTAS DEL AUTODIAGNÓSTICO (basado en ISO 19011 + ISO 23894)
# ══════════════════════════════════════════════════════════════════════════════

DIMENSIONES_AUTO = [
    {
        "nombre": "1. Gobernanza de IA",
        "descripcion": "Políticas, liderazgo y estructura organizacional para la IA (ISO 27001 Cláusula 5 / ISO 42001 Cláusula 5 / NIST GOVERN)",
        "preguntas": [
            {
                "id": "GOV-1",
                "texto": "¿Existe una política de IA aprobada por la alta dirección que defina principios éticos, niveles de autonomía y supervisión humana?",
                "opciones": [
                    ("No existe", 0),
                    ("En borrador", 1),
                    ("Existe pero no se aplica", 2),
                    ("Implementada parcialmente", 3),
                    ("Completamente implementada", 4),
                    ("Optimizada con mejora continua", 5),
                ]
            },
            {
                "id": "GOV-2",
                "texto": "¿Hay un responsable formal (CISO de IA / Oficial de IA) con autoridad para detener despliegues de modelos críticos?",
                "opciones": [
                    ("No hay responsable asignado", 0),
                    ("Rol definido pero sin autoridad formal", 1),
                    ("Rol asignado, autoridad limitada", 2),
                    ("Rol con autoridad para detener despliegues", 3),
                    ("Rol con autoridad + comité de ética de IA", 4),
                    ("Estructura de gobierno de IA madura con reporting directo a junta", 5),
                ]
            },
            {
                "id": "GOV-3",
                "texto": "¿Los roles y responsabilidades para sistemas de IA están formalmente definidos e integrados con el SGSI?",
                "opciones": [
                    ("No definidos", 0),
                    ("Definidos informalmente", 1),
                    ("Definidos pero no integrados con SGSI", 2),
                    ("Definidos e integrados parcialmente", 3),
                    ("Completamente integrados con SGSI", 4),
                    ("Integración total con auditoría independiente", 5),
                ]
            }
        ]
    },
    {
        "nombre": "2. Gestión de Riesgos de IA",
        "descripcion": "Identificación, evaluación y tratamiento de riesgos específicos de IA (ISO 27001 Cláusula 6.1 / ISO 42001 Cláusula 6.1 / NIST MAP-MEASURE / ISO 23894)",
        "preguntas": [
            {
                "id": "RIES-1",
                "texto": "¿El proceso de gestión de riesgos de la organización incluye riesgos específicos de IA (opacidad algorítmica, deriva del modelo, ataques adversariales)?",
                "opciones": [
                    ("No se consideran riesgos de IA", 0),
                    ("Identificados pero no evaluados", 1),
                    ("Evaluados informalmente", 2),
                    ("Evaluados con metodología definida", 3),
                    ("Integrados en el proceso de riesgos corporativo", 4),
                    ("Gestionados con monitoreo continuo y métricas cuantitativas", 5),
                ]
            },
            {
                "id": "RIES-2",
                "texto": "¿Se realiza evaluación de impacto de IA (AIF) antes del despliegue de nuevos modelos según ISO 42001 A.2?",
                "opciones": [
                    ("No se realiza", 0),
                    ("Ocasionalmente, sin metodología", 1),
                    ("Para modelos críticos, metodología básica", 2),
                    ("Para todos los modelos, metodología definida", 3),
                    ("Para todos los modelos, con revisión independiente", 4),
                    ("AIF obligatorio + revisión externa periódica", 5),
                ]
            },
            {
                "id": "RIES-3",
                "texto": "¿Se monitorea la deriva del modelo (Model Drift) y la degradación del rendimiento en producción?",
                "opciones": [
                    ("No se monitorea", 0),
                    ("Monitoreo manual esporádico", 1),
                    ("Monitoreo automatizado básico", 2),
                    ("Monitoreo automatizado con alertas", 3),
                    ("Monitoreo con dashboards y KPIs definidos", 4),
                    ("Monitoreo predictivo con acción correctiva automática", 5),
                ]
            },
            {
                "id": "RIES-4",
                "texto": "¿Se realizan pruebas de robustez adversarial a los modelos antes del despliegue?",
                "opciones": [
                    ("No se realizan", 0),
                    ("Pruebas básicas no sistemáticas", 1),
                    ("Pruebas para modelos críticos", 2),
                    ("Pruebas sistemáticas con metodología definida", 3),
                    ("Pruebas automatizadas en pipeline CI/CD", 4),
                    ("Red teaming de IA con periodicidad definida", 5),
                ]
            }
        ]
    },
    {
        "nombre": "3. Ciclo de Vida del Modelo",
        "descripcion": "Desarrollo seguro, validación y despliegue (ISO 27001 A.8.25-8.29 / ISO 42001 A.7 / NIST MAP 3.1-3.5)",
        "preguntas": [
            {
                "id": "CICLO-1",
                "texto": "¿El desarrollo de modelos sigue un proceso MLSecOps con controles de seguridad en cada etapa del pipeline?",
                "opciones": [
                    ("No hay proceso definido", 0),
                    ("Desarrollo informal sin controles de seguridad", 1),
                    ("MLOps básico, sin seguridad integrada", 2),
                    ("MLSecOps con controles en etapas clave", 3),
                    ("MLSecOps automatizado en CI/CD", 4),
                    ("MLSecOps maduro con security gates y validación continua", 5),
                ]
            },
            {
                "id": "CICLO-2",
                "texto": "¿Los datos de entrenamiento se validan para detectar sesgos, envenenamiento y calidad antes de su uso?",
                "opciones": [
                    ("No se validan", 0),
                    ("Validación manual básica", 1),
                    ("Validación automatizada de calidad", 2),
                    ("Validación de calidad + detección de sesgos", 3),
                    ("Validación completa con reportes de equidad", 4),
                    ("Validación continua con federated learning y privacidad diferencial", 5),
                ]
            },
            {
                "id": "CICLO-3",
                "texto": "¿Los modelos se registran con model cards, versionado y firmas criptográficas?",
                "opciones": [
                    ("No se registran", 0),
                    ("Registro manual básico", 1),
                    ("Model registry con versionado", 2),
                    ("Model registry + model cards", 3),
                    ("Model registry + model cards + firmas digitales", 4),
                    ("Model registry inmutable + SBOM de IA + firmas verificables", 5),
                ]
            }
        ]
    },
    {
        "nombre": "4. Seguridad Técnica del Modelo",
        "descripcion": "Protección de modelos, datos y APIs (ISO 27001 A.8.8, A.8.15, A.5.15 / ISO 42001 A.4 / NIST MANAGE 2.2)",
        "preguntas": [
            {
                "id": "TEC-1",
                "texto": "¿Las APIs de inferencia del modelo están protegidas con autenticación, rate limiting y validación de entrada?",
                "opciones": [
                    ("No hay APIs expuestas o no están protegidas", 0),
                    ("Autenticación básica sin rate limiting", 1),
                    ("Autenticación + rate limiting", 2),
                    ("Autenticación + rate limiting + validación de entrada", 3),
                    ("API Gateway con WAF y detección de anomalías", 4),
                    ("Protección completa con Zero Trust y monitoreo adversarial", 5),
                ]
            },
            {
                "id": "TEC-2",
                "texto": "¿Los logs de inferencia del modelo son inmutables y permiten trazabilidad forense completa?",
                "opciones": [
                    ("No se registran logs de inferencia", 0),
                    ("Logs básicos sin protección", 1),
                    ("Logs protegidos contra modificación", 2),
                    ("Logs inmutables con trazabilidad", 3),
                    ("Logs inmutables + correlación con eventos de seguridad", 4),
                    ("Sistema de logging blockchain/WORM con capacidad forense completa", 5),
                ]
            },
            {
                "id": "TEC-3",
                "texto": "¿El modelo y sus datos de entrenamiento están cifrados en reposo y en tránsito?",
                "opciones": [
                    ("No están cifrados", 0),
                    ("Cifrado en tránsito solamente", 1),
                    ("Cifrado en reposo y tránsito básico", 2),
                    ("Cifrado completo con gestión de claves (HSM)", 3),
                    ("Cifrado completo + firma de modelos", 4),
                    ("Cifrado completo + HSM + preparación post-cuántica", 5),
                ]
            },
            {
                "id": "TEC-4",
                "texto": "¿El control de acceso a los pipelines ML sigue el principio de Zero Trust?",
                "opciones": [
                    ("Acceso libre a entornos ML", 0),
                    ("Control de acceso básico por usuario", 1),
                    ("Segregación de entornos dev/staging/prod", 2),
                    ("Zero Trust con MFA para operaciones críticas", 3),
                    ("Zero Trust + aprobación multi-persona para despliegues", 4),
                    ("Zero Trust completo + just-in-time access + auditoría continua", 5),
                ]
            }
        ]
    },
    {
        "nombre": "5. Supervisión Humana y Transparencia",
        "descripcion": "Human-in-the-loop, explicabilidad y comunicación (ISO 27001 Cláusula 7.4, A.6.3 / ISO 42001 A.3 / NIST GOVERN 3.1)",
        "preguntas": [
            {
                "id": "HUM-1",
                "texto": "¿Las decisiones críticas automatizadas tienen un mecanismo formal de supervisión humana (Human-in-the-Loop)?",
                "opciones": [
                    ("Sin supervisión humana", 0),
                    ("Supervisión humana reactiva post-decisión", 1),
                    ("Human-on-the-loop (monitoreo sin intervención directa)", 2),
                    ("Human-in-the-loop para decisiones irreversibles", 3),
                    ("HITL con tiempos de respuesta validados", 4),
                    ("HITL + override documentado + métricas de efectividad", 5),
                ]
            },
            {
                "id": "HUM-2",
                "texto": "¿Los operadores y usuarios finales reciben capacitación sobre las capacidades y limitaciones del sistema de IA?",
                "opciones": [
                    ("No hay capacitación", 0),
                    ("Capacitación básica en el uso del sistema", 1),
                    ("Capacitación sobre capacidades y limitaciones", 2),
                    ("Capacitación + concientización sobre riesgos de IA", 3),
                    ("Programa de formación continua certificado", 4),
                    ("Formación + simulacros de fallo + certificación periódica", 5),
                ]
            },
            {
                "id": "HUM-3",
                "texto": "¿El modelo puede explicar sus decisiones de forma comprensible para los operadores (explicabilidad)?",
                "opciones": [
                    ("Sin capacidad de explicación", 0),
                    ("Explicabilidad básica (feature importance)", 1),
                    ("Explicabilidad con SHAP/LIME para auditoría", 2),
                    ("Explicabilidad en tiempo real para operadores", 3),
                    ("Explicabilidad en tiempo real + post-hoc para reguladores", 4),
                    ("Explicabilidad completa + reportes automáticos de auditoría", 5),
                ]
            },
            {
                "id": "HUM-4",
                "texto": "¿Se informa a los usuarios cuando interactúan con un sistema de IA (transparencia)?",
                "opciones": [
                    ("No se informa", 0),
                    ("Se informa en términos y condiciones", 1),
                    ("Se informa en el punto de interacción", 2),
                    ("Se informa + se explican las capacidades del sistema", 3),
                    ("Se informa + se ofrece canal de apelación", 4),
                    ("Disclosure completo + model cards públicos + canal de apelación", 5),
                ]
            }
        ]
    },
    {
        "nombre": "6. Monitoreo y Mejora Continua",
        "descripcion": "Métricas, auditoría y ciclo de mejora (ISO 27001 Cláusula 9-10 / ISO 42001 Cláusula 9-10 / NIST MEASURE / ISO 19011 Seguimiento)",
        "preguntas": [
            {
                "id": "MON-1",
                "texto": "¿Existe un dashboard de monitoreo continuo con KPIs de rendimiento, deriva, equidad y seguridad del modelo?",
                "opciones": [
                    ("No existe monitoreo", 0),
                    ("Monitoreo manual periódico", 1),
                    ("Dashboard básico con métricas técnicas", 2),
                    ("Dashboard con KPIs de rendimiento y deriva", 3),
                    ("Dashboard integral: rendimiento, deriva, equidad, seguridad", 4),
                    ("Dashboard con alertas predictivas y acción correctiva automatizada", 5),
                ]
            },
            {
                "id": "MON-2",
                "texto": "¿Se realizan auditorías periódicas de los sistemas de IA siguiendo la metodología ISO 19011?",
                "opciones": [
                    ("No se auditan", 0),
                    ("Auditorías reactivas post-incidente", 1),
                    ("Auditorías anuales básicas", 2),
                    ("Auditorías semestrales con checklist definido", 3),
                    ("Auditoría continua con herramientas automatizadas", 4),
                    ("Programa de auditoría maduro: continua + externa + certificable", 5),
                ]
            },
            {
                "id": "MON-3",
                "texto": "¿Existe un plan de continuidad operativa para fallos catastróficos de IA (modo degradado, RTO < 15 min)?",
                "opciones": [
                    ("No existe plan de continuidad", 0),
                    ("Plan básico sin pruebas", 1),
                    ("Plan documentado con RTO definido", 2),
                    ("Plan probado con simulacros anuales", 3),
                    ("Plan probado con simulacros semestrales + modo degradado validado", 4),
                    ("Plan maduro: hot standby, failover automático, simulacros trimestrales", 5),
                ]
            }
        ]
    },
    {
        "nombre": "7. Cadena de Suministro y Terceros",
        "descripcion": "Proveedores de IA, modelos externos y dependencias (ISO 27001 A.5.19-5.23 / ISO 42001 A.8 / NIST GOVERN 6.1-6.2)",
        "preguntas": [
            {
                "id": "CAD-1",
                "texto": "¿Los proveedores de modelos de IA (APIs, modelos pre-entrenados, datasets) son evaluados en seguridad?",
                "opciones": [
                    ("No se evalúan proveedores", 0),
                    ("Evaluación básica sin criterios definidos", 1),
                    ("Evaluación con cuestionario de seguridad", 2),
                    ("Evaluación con auditoría de proveedores", 3),
                    ("AI-SBOM obligatorio para todos los proveedores", 4),
                    ("AI-SBOM + auditoría in situ + cláusulas contractuales de seguridad", 5),
                ]
            },
            {
                "id": "CAD-2",
                "texto": "¿Se tiene un inventario completo de dependencias de IA (librerías, frameworks, modelos base)?",
                "opciones": [
                    ("No hay inventario", 0),
                    ("Inventario manual parcial", 1),
                    ("Inventario automatizado básico", 2),
                    ("SBOM de IA con versionado completo", 3),
                    ("SBOM + escaneo de vulnerabilidades automatizado", 4),
                    ("SBOM + escaneo + parcheo automatizado + vigilancia de amenazas", 5),
                ]
            }
        ]
    }
]


# ══════════════════════════════════════════════════════════════════════════════
# CÁLCULO DE MADUREZ
# ══════════════════════════════════════════════════════════════════════════════

def calcular_madurez(respuestas: dict) -> dict:
    """
    Calcula el nivel de madurez por dimensión y el puntaje general.
    Respuestas: {pregunta_id: valor_seleccionado (0-5)}
    Retorna: {dimensiones, puntajes, nivel_global, descripcion}
    """
    resultados = {}
    puntaje_total = 0
    maximo_total = 0

    for dim in DIMENSIONES_AUTO:
        puntaje_dim = 0
        maximo_dim = 0
        preguntas_dim = []

        for p in dim["preguntas"]:
            valor = respuestas.get(p["id"], 0)
            max_opcion = max(v for _, v in p["opciones"])
            puntaje_dim += valor
            maximo_dim += max_opcion
            preguntas_dim.append({
                "id": p["id"],
                "texto": p["texto"],
                "valor": valor,
                "maximo": max_opcion,
                "porcentaje": round(valor / max_opcion * 100, 1)
            })

        porcentaje_dim = round(puntaje_dim / maximo_dim * 100, 1) if maximo_dim > 0 else 0
        nivel_dim = _nivel_madurez(porcentaje_dim)

        resultados[dim["nombre"]] = {
            "puntaje": puntaje_dim,
            "maximo": maximo_dim,
            "porcentaje": porcentaje_dim,
            "nivel": nivel_dim,
            "preguntas": preguntas_dim
        }

        puntaje_total += puntaje_dim
        maximo_total += maximo_dim

    porcentaje_global = round(puntaje_total / maximo_total * 100, 1) if maximo_total > 0 else 0
    nivel_global = _nivel_madurez(porcentaje_global)

    return {
        "dimensiones": resultados,
        "puntaje_total": puntaje_total,
        "maximo_total": maximo_total,
        "porcentaje_global": porcentaje_global,
        "nivel_global": nivel_global,
        "descripcion_global": _descripcion_global(nivel_global, porcentaje_global)
    }


def _nivel_madurez(porcentaje: float) -> str:
    if porcentaje >= 90:
        return "Optimizado"
    elif porcentaje >= 70:
        return "Gestionado"
    elif porcentaje >= 50:
        return "Definido"
    elif porcentaje >= 30:
        return "Repetible"
    elif porcentaje >= 10:
        return "Inicial"
    else:
        return "Inexistente"


def _descripcion_global(nivel: str, pct: float) -> str:
    desc = {
        "Inexistente": "La organización no ha comenzado a gestionar los riesgos de IA. No hay procesos, roles ni controles definidos. Exposición crítica a incidentes.",
        "Inicial": "La organización reconoce la necesidad de gestionar IA pero lo hace de forma reactiva y dependiente de personas clave. Sin procesos estandarizados.",
        "Repetible": "Existen procesos básicos que se aplican de forma inconsistente. Alta dependencia de personas. La documentación es parcial.",
        "Definido": "Los procesos están documentados, estandarizados y se aplican consistentemente. Los controles están implementados pero no se miden sistemáticamente.",
        "Gestionado": "Los controles se monitorean con métricas cuantitativas. Hay mejora continua basada en datos. La organización está preparada para certificación.",
        "Optimizado": "La gestión de IA está completamente integrada en la cultura organizacional. Automatización, mejora continua y auditoría independiente. Referente del sector."
    }
    return desc.get(nivel, "")


# ══════════════════════════════════════════════════════════════════════════════
# GENERACIÓN DE PROPUESTA BASADA EN RESULTADOS
# ══════════════════════════════════════════════════════════════════════════════

def generar_prompt_propuesta(resultados: dict, sector: str, contexto: str) -> str:
    """
    Genera el prompt para el LLM basado en los resultados del autodiagnóstico.
    La propuesta sigue la metodología ISO 19011 (5 fases) e incluye ISO 23894.
    """
    dim_desc = []
    for dim_nombre, dim_data in resultados["dimensiones"].items():
        areas_bajas = [p["texto"][:80] for p in dim_data["preguntas"] if p["porcentaje"] < 50]
        areas_medias = [p["texto"][:80] for p in dim_data["preguntas"] if 50 <= p["porcentaje"] < 80]
        dim_desc.append(f"""
### {dim_nombre} — {dim_data['nivel']} ({dim_data['porcentaje']}%)
- Puntaje: {dim_data['puntaje']}/{dim_data['maximo']}
- Áreas críticas (menos de 50%):
{chr(10).join('  - ❌ ' + a for a in areas_bajas) if areas_bajas else '  - Ninguna'}
- Áreas en desarrollo (50-80%):
{chr(10).join('  - ⚠️ ' + a for a in areas_medias) if areas_medias else '  - Ninguna'}
""")

    dim_texto = "\n".join(dim_desc)

    prompt = f"""Eres un consultor senior en ciberseguridad e IA para infraestructura crítica.
Basado en los siguientes resultados de autodiagnóstico de madurez, genera una **Propuesta de Implementación** detallada.

## Resultados del Autodiagnóstico IA-SEC

**Nivel de Madurez Global: {resultados['nivel_global']} ({resultados['porcentaje_global']}%)**
{resultados['descripcion_global']}

**Sector:** {sector}
**Contexto organizacional:** {contexto}

## Desglose por Dimensión:
{dim_texto}

## INSTRUCCIONES — Estructura obligatoria:

Genera la propuesta siguiendo la metodología ISO 19011:2018 con las siguientes secciones:

1. **Resumen Ejecutivo** — Nivel de madurez global, hallazgos principales, urgencia.
2. **Metodología Aplicada** — ISO 19011 (5 fases de auditoría) + ISO 23894 (gestión de riesgos de IA).
3. **Catálogo de Riesgos Identificados** (ISO 23894:2023): Opacidad algorítmica, Deriva del modelo, Vulnerabilidad adversarial, Sesgo algorítmico, Privacidad, Impacto social, Seguridad física. Indicar cuáles aplican según los resultados.
4. **Hoja de Ruta de Implementación** por fases (Fase 1: 0-3m, Fase 2: 3-6m, Fase 3: 6-12m).
5. **Priorización de Controles** — Basada en las dimensiones con menor puntaje.
6. **Arquitectura de Seguridad de IA recomendada**.
7. **KPIs y Métricas de Monitoreo** (ISO 23894 Cláusula 6.2).
8. **Quick Wins** — Acciones inmediatas (primeras 2 semanas).
9. **Plan de Seguimiento** — Próximas auditorías, frecuencia de revisión.

Formato: Markdown estructurado con emojis. Enfocado en acción y resultados medibles."""
    return prompt


# ══════════════════════════════════════════════════════════════════════════════
# INTERFAZ STREAMLIT
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_autodiagnostico():
    """Pestaña completa de autodiagnóstico de madurez de IA."""
    st.markdown("#### 🔬 Autodiagnóstico de Madurez IA-SEC")
    st.markdown("""
    **Evalúa la madurez de tu organización en la gestión de sistemas de IA**  
    Basado en ISO 27001 · ISO 42001 · NIST AI RMF · ISO 19011 · ISO 23894

    Responde el cuestionario por dimensión. Al finalizar, obtendrás:
    - Nivel de madurez global y por dimensión (escala MSPI 6 niveles)
    - Propuesta de implementación generada por IA siguiendo ISO 19011
    - Catálogo de riesgos según ISO 23894
    """)

    if "auto_respuestas" not in st.session_state:
        st.session_state.auto_respuestas = {}
    if "auto_resultados" not in st.session_state:
        st.session_state.auto_resultados = None
    if "auto_propuesta" not in st.session_state:
        st.session_state.auto_propuesta = None

    tab_preguntas, tab_resultados, tab_propuesta = st.tabs([
        "📝 Cuestionario", "📊 Resultados de Madurez", "📄 Propuesta de Implementación"
    ])

    with tab_preguntas:
        st.markdown("### Cuestionario de Autodiagnóstico")
        st.markdown("Responde cada pregunta seleccionando la opción que mejor describa el estado actual de tu organización.")

        sector_auto = st.text_input(
            "🏭 Sector / Industria",
            placeholder="Ej: Salud, Finanzas, Energía, Telecomunicaciones...",
            key="auto_sector"
        )
        contexto_auto = st.text_area(
            "📋 Contexto organizacional",
            placeholder="Describe brevemente la organización: tamaño, tipo de sistemas de IA que utiliza, madurez actual...",
            height=80,
            key="auto_contexto"
        )

        respuestas = {}
        for dim in DIMENSIONES_AUTO:
            with st.expander(f"**{dim['nombre']}** — {dim['descripcion']}", expanded=True):
                for p in dim["preguntas"]:
                    opciones = [o[0] for o in p["opciones"]]
                    valores = {o[0]: o[1] for o in p["opciones"]}
                    idx_default = 0
                    saved = st.session_state.auto_respuestas.get(p["id"], None)
                    if saved is not None:
                        for i, o in enumerate(p["opciones"]):
                            if o[1] == saved:
                                idx_default = i
                                break
                    seleccion = st.radio(
                        p["texto"],
                        opciones,
                        index=idx_default,
                        key=f"auto_{p['id']}"
                    )
                    respuestas[p["id"]] = valores[seleccion]

        st.session_state.auto_respuestas = respuestas

        col_calc, col_clear = st.columns([1, 1])
        with col_calc:
            if st.button("🔬 Calcular Madurez", type="primary", use_container_width=True):
                resultados = calcular_madurez(respuestas)
                st.session_state.auto_resultados = resultados
                st.success(f"✅ Madurez calculada: **{resultados['nivel_global']}** ({resultados['porcentaje_global']}%)")
                st.balloons()

        with col_clear:
            if st.button("🔄 Reiniciar cuestionario", use_container_width=True):
                st.session_state.auto_respuestas = {}
                st.session_state.auto_resultados = None
                st.session_state.auto_propuesta = None
                st.rerun()

    with tab_resultados:
        if st.session_state.auto_resultados is None:
            st.info("Completa el cuestionario en la pestaña **📝 Cuestionario** y presiona 'Calcular Madurez'.")
        else:
            res = st.session_state.auto_resultados
            st.markdown(f"### 📊 Nivel de Madurez Global: **{res['nivel_global']}**")
            st.markdown(f"**{res['porcentaje_global']}%** — {res['descripcion_global']}")

            import pandas as pd
            dim_data = []
            for dim_nombre, dim_res in res["dimensiones"].items():
                dim_data.append({
                    "Dimensión": dim_nombre,
                    "Madurez": dim_res["nivel"],
                    "Puntaje": f"{dim_res['puntaje']}/{dim_res['maximo']}",
                    "%": dim_res["porcentaje"]
                })
            df_dim = pd.DataFrame(dim_data)
            st.dataframe(df_dim, use_container_width=True, hide_index=True,
                         column_config={
                             "Dimensión": st.column_config.TextColumn("Dimensión", width="large"),
                             "Madurez": st.column_config.TextColumn("Nivel", width="medium"),
                             "Puntaje": st.column_config.TextColumn("Puntaje", width="small"),
                             "%": st.column_config.ProgressColumn("%", format="%.1f%%", width="medium")
                         })

            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[res["dimensiones"][d]["porcentaje"] for d in res["dimensiones"]],
                theta=list(res["dimensiones"].keys()),
                fill='toself',
                name='Madurez IA-SEC',
                line_color='#7c3aed'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Desglose por Dimensión")
            for dim_nombre, dim_res in res["dimensiones"].items():
                with st.expander(f"{dim_nombre} — {dim_res['nivel']} ({dim_res['porcentaje']}%)"):
                    for p in dim_res["preguntas"]:
                        color = "🟢" if p["porcentaje"] >= 80 else "🟡" if p["porcentaje"] >= 50 else "🔴"
                        st.markdown(f"{color} **{p['texto'][:100]}...** — {p['valor']}/{p['maximo']} ({p['porcentaje']}%)")

            col_prop, _ = st.columns([1, 2])
            with col_prop:
                if st.button("🚀 Generar Propuesta desde Resultados", type="primary", use_container_width=True):
                    s_auto = st.session_state.get("auto_sector", "").strip()
                    c_auto = st.session_state.get("auto_contexto", "").strip()
                    if not s_auto:
                        st.warning("Ingresa el sector en el cuestionario antes de generar la propuesta.")
                    elif not c_auto:
                        st.warning("Ingresa el contexto organizacional en el cuestionario antes de generar la propuesta.")
                    else:
                        prompt = generar_prompt_propuesta(res, s_auto, c_auto)
                        st.session_state.auto_prompt = prompt
                        st.session_state.auto_propuesta = "PENDIENTE"
                        st.info("Ve a la pestaña **📄 Propuesta de Implementación** y usa el botón para generar con el asistente IA.")

    with tab_propuesta:
        if st.session_state.auto_propuesta is None:
            st.info("Primero completa el cuestionario y calcula la madurez, luego genera la propuesta desde la pestaña de resultados.")
        elif st.session_state.auto_propuesta == "PENDIENTE":
            prompt = st.session_state.get("auto_prompt", "")
            st.markdown("### 📄 Propuesta de Implementación")
            st.markdown("**Metodología:** ISO 19011:2018 (5 fases) + ISO 23894:2023 (gestión de riesgos de IA)")

            col_ia, col_md, col_pdf = st.columns([1, 1, 1])
            with col_ia:
                if st.button("🤖 Generar con Asistente IA", type="primary", use_container_width=True):
                    st.session_state["generar_auto_propuesta"] = True
                    st.rerun()
        else:
            st.markdown("### 📄 Propuesta de Implementación")
            st.markdown(st.session_state.auto_propuesta)
            col_md, col_xls, col_pdf = st.columns(3)
            with col_md:
                st.download_button(
                    "📄 .md", data=st.session_state.auto_propuesta,
                    file_name="autodiagnostico_propuesta.md",
                    mime="text/markdown", key="dl_auto_prop_md",
                    use_container_width=True)
            with col_xls:
                try:
                    from openpyxl import Workbook
                    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
                    import tempfile, os

                    wb = Workbook()
                    thin_border = Border(left=Side(style="thin", color="334155"), right=Side(style="thin", color="334155"),
                                         top=Side(style="thin", color="334155"), bottom=Side(style="thin", color="334155"))
                    dark_fill = PatternFill(start_color="1a1a2e", end_color="1a1a2e", fill_type="solid")
                    accent_fill = PatternFill(start_color="0f3460", end_color="0f3460", fill_type="solid")
                    header_fill = PatternFill(start_color="16213e", end_color="16213e", fill_type="solid")
                    title_font = Font(name="Century Gothic", size=16, bold=True, color="FFFFFF")
                    header_font = Font(name="Century Gothic", size=9, bold=True, color="FFFFFF")
                    data_font = Font(name="Century Gothic", size=8, color="E0E0E0")

                    # Portada
                    ws = wb.active
                    ws.title = "Portada"
                    ws.merge_cells("A1:F1")
                    ws["A1"] = "PROPUESTA DE IMPLEMENTACIÓN — AUTODIAGNÓSTICO"
                    ws["A1"].font = title_font; ws["A1"].fill = dark_fill
                    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
                    ws.row_dimensions[1].height = 45

                    meta = [
                        ("Sector", st.session_state.get("auto_sector", "General")),
                        ("Empresa", st.session_state.get("auto_empresa", "No especificada")),
                        ("Nivel Madurez", f"{st.session_state.get('auto_puntaje_global', 0)}%"),
                        ("Fecha", __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M")),
                    ]
                    for i, (label, val) in enumerate(meta, 4):
                        ws.cell(row=i, column=1, value=label).font = Font(name="Century Gothic", size=9, bold=True, color="58C8F2")
                        ws.cell(row=i, column=1).fill = header_fill; ws.cell(row=i, column=1).border = thin_border
                        ws.merge_cells(f"A{i}:B{i}")
                        c = ws.cell(row=i, column=3, value=val)
                        c.font = Font(name="Century Gothic", size=9, color="E0E0E0")
                        c.fill = accent_fill; c.border = thin_border
                        ws.merge_cells(f"C{i}:F{i}")

                    # Propuesta completa
                    ws2 = wb.create_sheet("Propuesta Completa")
                    ws2.sheet_properties.tabColor = "58C8F2"
                    ws2.merge_cells("A1:B1")
                    ws2["A1"] = "PROPUESTA DE IMPLEMENTACIÓN — TEXTO COMPLETO"
                    ws2["A1"].font = Font(name="Century Gothic", size=12, bold=True, color="FFFFFF")
                    ws2["A1"].fill = dark_fill; ws2["A1"].alignment = Alignment(horizontal="center")
                    ws2.row_dimensions[1].height = 30

                    lines = st.session_state.auto_propuesta.split("\n")
                    for i, line in enumerate(lines):
                        r = 3 + i
                        ws2.merge_cells(f"A{r}:B{r}")
                        ws2.cell(row=r, column=1, value=line).font = Font(name="Consolas", size=7, color="E0E0E0")
                        ws2.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
                    ws2.column_dimensions["A"].width = 100; ws2.column_dimensions["B"].width = 30

                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                    wb.save(tmp.name); tmp.close()
                    with open(tmp.name, "rb") as f: excel_bytes = f.read()
                    os.unlink(tmp.name)

                    st.download_button("📊 Excel + Propuesta", data=excel_bytes,
                        file_name="autodiagnostico_propuesta.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_auto_prop_xls", type="primary", use_container_width=True)
                except Exception as e:
                    st.caption(f"Excel no disponible: {e}")

            with col_pdf:
                from pdf_export import generar_pdf_propuesta_interoperabilidad
                try:
                    s_auto = st.session_state.get("auto_sector", "No especificado")
                    pdf_bytes = generar_pdf_propuesta_interoperabilidad(
                        st.session_state.auto_propuesta, "autodiag", s_auto,
                        {"auto": "evaluado"}, "autodiagnostico", "AuditAI Pro", "autodiagnóstico"
                    )
                    st.download_button(
                        "📄 PDF", data=pdf_bytes,
                        file_name="autodiagnostico_propuesta.pdf",
                        mime="application/pdf", key="dl_auto_prop_pdf",
                        use_container_width=True)
                except Exception as e:
                    st.caption(f"PDF no disponible: {e}")
