"""
Módulo de Guía del Auditor IA-SEC
Integra ISO 19011:2018 (Directrices para auditar sistemas de gestión)
e ISO/IEC 23894:2023 (Gestión de riesgos de IA)
Como base de conocimiento para fortalecer el rol del auditor.
"""
import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
# ISO 19011:2018 — Directrices para la auditoría de sistemas de gestión
# ══════════════════════════════════════════════════════════════════════════════

PRINCIPIOS_AUDITORIA = [
    {
        "principio": "Integridad",
        "descripcion": "Los auditores deben actuar con honestidad, diligencia y responsabilidad, cumpliendo con los requisitos aplicables y manteniendo la confidencialidad de la información.",
        "aplicacion_ic": "En infraestructura crítica, la integridad del auditor es fundamental dado que los hallazgos pueden tener implicaciones de seguridad nacional."
    },
    {
        "principio": "Presentación imparcial",
        "descripcion": "Los hallazgos, conclusiones e informes deben reflejar de manera veraz y precisa las actividades de auditoría, reportando obstáculos significativos y opiniones divergentes no resueltas.",
        "aplicacion_ic": "El auditor debe reportar con objetividad incluso cuando los hallazgos impliquen detener operaciones críticas."
    },
    {
        "principio": "Debido cuidado profesional",
        "descripcion": "Los auditores deben aplicar la diligencia y el juicio profesional necesarios, utilizando la capacidad de tomar decisiones informadas en situaciones de auditoría.",
        "aplicacion_ic": "En sistemas de IA, el auditor debe entender las limitaciones del modelo para evaluar riesgos sin caer en falsa confianza."
    },
    {
        "principio": "Confidencialidad",
        "descripcion": "Los auditores deben ser cautelosos en el uso y protección de la información obtenida durante la auditoría, no divulgándola sin la autorización del cliente.",
        "aplicacion_ic": "Los datos de entrenamiento, arquitectura de modelos y vulnerabilidades de IA descubiertas son información altamente sensible."
    },
    {
        "principio": "Independencia",
        "descripcion": "Los auditores deben ser independientes de la actividad auditada para garantizar imparcialidad y objetividad en las conclusiones.",
        "aplicacion_ic": "El equipo auditor de IA debe estar separado del equipo de desarrollo del modelo para evitar conflictos de interés."
    },
    {
        "principio": "Enfoque basado en evidencia",
        "descripcion": "La evidencia de auditoría debe ser verificable y basarse en muestras de información disponible. El uso apropiado de muestreo está relacionado con la confianza en las conclusiones.",
        "aplicacion_ic": "En IA, la evidencia incluye logs de inferencia, métricas de drift, resultados de testing adversarial y reportes de sesgo."
    }
]

FASES_AUDITORIA = [
    {
        "fase": "1. Iniciación",
        "clausula_19011": "6.2",
        "actividades": [
            "Establecer contacto inicial con el auditado",
            "Determinar la viabilidad de la auditoría",
            "Designar el equipo auditor y roles",
            "Definir objetivos, alcance y criterios"
        ],
        "entregables": ["Designación del equipo auditor", "Matriz de alcance y criterios"],
        "checklist_ia": [
            "¿El alcance incluye sistemas de IA en producción?",
            "¿Se identificaron los modelos de IA críticos?",
            "¿El equipo auditor incluye expertos en IA?"
        ]
    },
    {
        "fase": "2. Preparación",
        "clausula_19011": "6.3",
        "actividades": [
            "Revisar documentos del auditado (políticas, procedimientos, registros)",
            "Elaborar el plan de auditoría",
            "Preparar documentos de trabajo (checklists, listas de muestreo)",
            "Comunicar el plan al auditado"
        ],
        "entregables": ["Plan de auditoría", "Checklist de controles", "Lista de documentos a revisar"],
        "checklist_ia": [
            "¿Se revisaron los model cards y datasheets de los sistemas IA?",
            "¿Están disponibles los reportes de pruebas adversariales?",
            "¿Se prepararon preguntas específicas sobre gobernanza de IA?"
        ]
    },
    {
        "fase": "3. Ejecución",
        "clausula_19011": "6.4",
        "actividades": [
            "Realizar la reunión de apertura",
            "Recolectar y verificar evidencia (entrevistas, observaciones, revisión documental)",
            "Generar hallazgos de auditoría (conformidades, no conformidades, oportunidades de mejora)",
            "Realizar la reunión de cierre"
        ],
        "entregables": ["Evidencia documentada", "Hallazgos preliminares", "Minuta de reunión de cierre"],
        "checklist_ia": [
            "¿Se verificaron logs de inferencia del modelo?",
            "¿Se entrevistó al responsable de supervisión de IA?",
            "¿Se observó el funcionamiento del modelo en producción?",
            "¿Se revisaron los reportes de monitoreo de drift?"
        ]
    },
    {
        "fase": "4. Informe",
        "clausula_19011": "6.5",
        "actividades": [
            "Redactar el informe de auditoría (hallazgos, conclusiones, recomendaciones)",
            "Revisar y aprobar el informe",
            "Distribuir el informe al cliente y al auditado",
            "Preservar la información documentada como evidencia"
        ],
        "entregables": ["Informe de auditoría", "Matriz de hallazgos", "Plan de acciones correctivas"],
        "checklist_ia": [
            "¿El informe incluye el nivel de madurez por cada dominio IA-SEC?",
            "¿Se documentaron los riesgos de IA identificados (opacidad, drift, adversarial)?",
            "¿Las recomendaciones priorizan los controles de gobernanza?"
        ]
    },
    {
        "fase": "5. Seguimiento",
        "clausula_19011": "6.6",
        "actividades": [
            "Verificar la implementación de acciones correctivas",
            "Realizar auditorías de seguimiento si es necesario",
            "Cerrar el ciclo de auditoría",
            "Actualizar el programa de auditoría"
        ],
        "entregables": ["Reporte de verificación de acciones", "Cierre de no conformidades", "Plan de próxima auditoría"],
        "checklist_ia": [
            "¿Se implementaron los controles correctivos en los modelos de IA?",
            "¿Se volvieron a probar los modelos después de las correcciones?",
            "¿Las lecciones aprendidas se incorporaron al programa de auditoría?"
        ]
    }
]

COMPETENCIAS_AUDITOR_IA = [
    {
        "area": "Conocimiento de normas",
        "descripcion": "Dominio de ISO 19011, ISO 27001, ISO 42001, NIST AI RMF",
        "nivel_requerido": "Avanzado",
        "como_obtenerlo": "Capacitación formal, cursos de auditor líder, participación en auditorías reales"
    },
    {
        "area": "Comprensión de IA/ML",
        "descripcion": "Ciclo de vida de ML, opacidad algorítmica, deriva de modelos, ataques adversariales, sesgo y equidad",
        "nivel_requerido": "Intermedio",
        "como_obtenerlo": "Curso de fundamentos de IA, taller de auditoría de algoritmos, lectura de ISO 23894"
    },
    {
        "area": "Seguridad de la información",
        "descripcion": "Sectores priorizados por CONPES 3995 (salud, finanzas, energía, telecomunicaciones, transporte)",
        "nivel_requerido": "Medio",
        "como_obtenerlo": "Estudio del CONPES 3995/4144, familiarización con regulaciones sectoriales"
    },
    {
        "area": "Gestión de riesgos",
        "descripcion": "ISO 31000, ISO 27005, ISO 23894 — Evaluación cualitativa y cuantitativa de riesgos de IA",
        "nivel_requerido": "Avanzado",
        "como_obtenerlo": "Curso de gestión de riesgos, práctica con matriz de probabilidad e impacto, ISO 23894"
    },
    {
        "area": "Comunicación y liderazgo",
        "descripcion": "Entrevistas, reuniones de apertura/cierre, redacción de informes ejecutivos",
        "nivel_requerido": "Avanzado",
        "como_obtenerlo": "Práctica supervisada, retroalimentación de auditores senior"
    }
]


# ══════════════════════════════════════════════════════════════════════════════
# ISO/IEC 23894:2023 — Gestión de riesgos de IA
# ══════════════════════════════════════════════════════════════════════════════

RIESGOS_IA_23894 = [
    {
        "id": "R-OPA",
        "riesgo": "Opacidad algorítmica",
        "clausula_23894": "5.3",
        "descripcion": "Imposibilidad de entender cómo el modelo llega a sus decisiones. La 'caja negra' impide auditar la lógica interna.",
        "controles_27001": ["A.8.15 — Logging", "Cláusula 10.2 — Acción correctiva"],
        "controles_42001": ["A.6.2.4 — Explicabilidad"],
        "ejemplo_salud": "Un sistema de diagnóstico por imágenes clasifica un tumor como benigno sin que el radiólogo pueda saber por qué."
    },
    {
        "id": "R-DER",
        "riesgo": "Deriva del modelo (Model Drift)",
        "clausula_23894": "5.4",
        "descripcion": "Degradación gradual del rendimiento del modelo cuando los datos de entrada cambian con el tiempo. No hay fallo binario sino deterioro silencioso.",
        "controles_27001": ["A.8.16 — Monitoreo", "Cláusula 8.2 — Evaluación periódica"],
        "controles_42001": ["A.6 — Monitoreo continuo", "A.9 — Evaluación desempeño"],
        "ejemplo_salud": "Un modelo de triage de urgencias entrenado en 2022 subestima pacientes COVID en 2025 porque la población cambió."
    },
    {
        "id": "R-ADV",
        "riesgo": "Vulnerabilidad adversarial",
        "clausula_23894": "5.5",
        "descripcion": "Atacantes manipulan entradas del modelo para inducir errores. Los controles de seguridad tradicionales no detectan estas manipulaciones.",
        "controles_27001": ["A.8.8 — Gestión de vulnerabilidades", "A.8.28 — Desarrollo seguro"],
        "controles_42001": ["A.7 — Desarrollo seguro de IA"],
        "ejemplo_salud": "Un atacante modifica píxeles en una radiografía para que el modelo clasifique un tumor como tejido sano."
    },
    {
        "id": "R-SES",
        "riesgo": "Sesgo algorítmico",
        "clausula_23894": "6.1",
        "descripcion": "El modelo produce resultados sistemáticamente desfavorables para grupos protegidos debido a datos de entrenamiento no representativos.",
        "controles_27001": ["Cláusula 4.2 — Partes interesadas"],
        "controles_42001": ["Anexo B — Impacto social", "A.1 — Requisitos éticos"],
        "ejemplo_salud": "Un algoritmo de priorización de trasplantes subestima pacientes de ciertos grupos étnicos."
    },
    {
        "id": "R-PRI",
        "riesgo": "Privacidad y protección de datos",
        "clausula_23894": "6.2",
        "descripcion": "El modelo puede memorizar datos sensibles de entrenamiento y reproducirlos en inferencia, filtrando información confidencial.",
        "controles_27001": ["A.8.12 — DLP", "A.8.10 — Eliminación"],
        "controles_42001": ["A.5 — Datos para IA"],
        "ejemplo_salud": "Un modelo de lenguaje clínico reproduce datos de historias clínicas de pacientes en sus respuestas."
    },
    {
        "id": "R-SOC",
        "riesgo": "Impacto social y reputacional",
        "clausula_23894": "6.3",
        "descripcion": "El despliegue de IA afecta la confianza pública, la equidad social y la percepción de la organización ante la comunidad.",
        "controles_27001": ["Cláusula 7.4 — Comunicación"],
        "controles_42001": ["A.2 — Evaluación de impacto", "Anexo B.3 — Transparencia"],
        "ejemplo_salud": "Un hospital implementa triage automatizado sin informar a los pacientes, generando desconfianza en la comunidad."
    },
    {
        "id": "R-SEG",
        "riesgo": "Seguridad física y funcional",
        "clausula_23894": "6.4",
        "descripcion": "Fallos en sistemas de IA pueden causar daños físicos a personas o infraestructura, especialmente en entornos de salud, energía o transporte.",
        "controles_27001": ["A.5.30 — Continuidad", "A.5.24-5.28 — Incidentes"],
        "controles_42001": ["A.6.2.5 — Continuidad de IA"],
        "ejemplo_salud": "Un robot quirúrgico con IA mal calibrado realiza movimientos incorrectos durante una operación."
    }
]

PROCESO_GESTION_RIESGOS_23894 = [
    {
        "fase": "Identificación de riesgos",
        "clausula": "6.1.2",
        "actividades": "Identificar los riesgos asociados con los sistemas de IA, incluyendo opacidad, drift, adversarial, sesgo y privacidad.",
        "tecnicas": "Brainstorming con equipo multidisciplinario, análisis de escenarios, revisión de incidentes previos, mapeo de partes interesadas.",
        "salidas": "Registro de riesgos de IA, matriz de causas y consecuencias."
    },
    {
        "fase": "Análisis de riesgos",
        "clausula": "6.1.3",
        "actividades": "Analizar la probabilidad y el impacto potencial de cada riesgo identificado, utilizando escalas cualitativas o cuantitativas.",
        "tecnicas": "Matriz de probabilidad e impacto (4×4), análisis de modo de fallo (FMEA), simulación de Monte Carlo, árbol de decisiones.",
        "salidas": "Nivel de riesgo inherente para cada riesgo identificado."
    },
    {
        "fase": "Evaluación de riesgos",
        "clausula": "6.1.4",
        "actividades": "Comparar los niveles de riesgo con los criterios de riesgo establecidos para determinar prioridades de tratamiento.",
        "tecnicas": "Comparación contra apetito de riesgo, definición de umbrales de criticidad, priorización por valor de riesgo.",
        "salidas": "Riesgos priorizados, decisión de tratar, tolerar, transferir o terminar."
    },
    {
        "fase": "Tratamiento de riesgos",
        "clausula": "6.1.5",
        "actividades": "Seleccionar e implementar opciones de tratamiento: evitar, reducir,转移 (transferir), aceptar, o compartir el riesgo.",
        "tecnicas": "Selección de controles del Anexo A de ISO 42001, implementación de barreras técnicas y administrativas, planes de contingencia.",
        "salidas": "Plan de tratamiento de riesgos de IA, controles implementados, riesgo residual documentado."
    },
    {
        "fase": "Monitoreo y revisión",
        "clausula": "6.2",
        "actividades": "Monitorear periódicamente los riesgos y la efectividad de los controles, actualizando el registro de riesgos según cambios en el entorno.",
        "tecnicas": "Indicadores de riesgo (KRI), dashboard de monitoreo continuo, auditorías periódicas, revisión de incidentes.",
        "salidas": "Reporte periódico de estado de riesgos, actualización del registro de riesgos."
    },
    {
        "fase": "Comunicación y consulta",
        "clausula": "6.3",
        "actividades": "Comunicar los riesgos de IA a las partes interesadas relevantes, incluyendo dirección, usuarios afectados y reguladores.",
        "tecnicas": "Reportes ejecutivos, disclosure a usuarios, canales de denuncia, reuniones con stakeholders.",
        "salidas": "Registro de comunicaciones, reportes de transparencia, canal de apelaciones."
    }
]


# ══════════════════════════════════════════════════════════════════════════════
# SECCIONES DE LA INTERFAZ
# ══════════════════════════════════════════════════════════════════════════════

def mostrar_rol_auditor():
    """Pestaña completa de Rol del Auditor con ISO 19011 y base de conocimiento."""
    st.markdown("#### 🎓 Rol del Auditor IA-SEC")
    st.markdown("""
    **ISO 19011:2018** — Directrices para la auditoría de sistemas de gestión  
    **ISO/IEC 23894:2023** — Gestión de riesgos de inteligencia artificial  
    **CONPES 3995 / 4144** — Política Nacional de Confianza Digital y Política de IA de Colombia
    """)

    tab_rol = st.tabs([
        "📋 Principios del Auditor",
        "📅 Ciclo de Auditoría (ISO 19011)",
        "🛡️ Gestión de Riesgos de IA (ISO 23894)",
        "🔍 Base de Conocimiento",
        "🎯 Competencias del Auditor IA"
    ])

    with tab_rol[0]:
        st.markdown("### Principios de Auditoría — ISO 19011 Cláusula 4")
        st.markdown("Estos seis principios son **obligatorios** para cualquier auditoría de sistemas de gestión, incluyendo IA.")
        for p in PRINCIPIOS_AUDITORIA:
            with st.expander(f"**{p['principio']}**"):
                st.info(f"**Aplicación:** {p['aplicacion_ic']}")

    with tab_rol[1]:
        st.markdown("### Ciclo de Auditoría — ISO 19011 Cláusula 6")
        st.markdown("El proceso de auditoría se divide en 5 fases secuenciales. Cada fase tiene actividades, entregables y un checklist específico para IA.")
        for fase in FASES_AUDITORIA:
            with st.expander(f"**{fase['fase']}** (ISO 19011 Cláusula {fase['clausula_19011']})"):
                st.markdown("**Actividades:**")
                for act in fase['actividades']:
                    st.markdown(f"- {act}")
                st.markdown("**Entregables:**")
                for ent in fase['entregables']:
                    st.markdown(f"- {ent}")
                st.markdown("**Checklist para IA:**")
                for chk in fase['checklist_ia']:
                    st.markdown(f"- ✅ {chk}")

        st.markdown("---")
        with st.expander("📥 Plantilla de Plan de Auditoría IA-SEC"):
            st.markdown("""
            ```
            PLAN DE AUDITORÍA IA-SEC
            ==========================
            Cliente: [Nombre de la organización]
            Fecha: [DD/MM/AAAA]
            Duración estimada: [N] días
            Equipo auditor: [Nombres y roles]
            
            Objetivos:
            1. Evaluar la conformidad del SGSI/SGIA con ISO 27001/42001
            2. Evaluar la gestión de riesgos de IA según ISO 23894
            3. Identificar brechas en controles según ISO 27001 e ISO 27002
            
            Alcance:
            - Sistemas de IA: [Listar modelos críticos]
            - Procesos: [Desarrollo, operación, monitoreo]
            - Instalaciones: [Ubicaciones a visitar]
            
            Criterios:
            - ISO/IEC 27001:2022 (Cláusulas 4-10, Anexo A)
            - ISO/IEC 42001:2023 (Cláusulas 4-10, Anexo A)
            - NIST AI RMF 1.0 (GOVERN, MAP, MEASURE, MANAGE)
            - ISO 19011:2018 (Metodología de auditoría)
            - ISO 23894:2023 (Gestión de riesgos de IA)
            
            Cronograma:
            Día 1: Reunión apertura + Revisión documental (Gobernanza)
            Día 2: Evaluación técnica (Ciclo de vida del modelo)
            Día 3: Verificación en producción + Entrevistas
            Día 4: Preparación de informes + Reunión de cierre
            ```
            """)

    with tab_rol[2]:
        st.markdown("### Gestión de Riesgos de IA — ISO/IEC 23894:2023")
        st.markdown("""
        La ISO 23894 complementa a ISO 27005 (gestión de riesgos de seguridad) con los **riesgos específicos de inteligencia artificial**.
        Se integra directamente con el proceso de evaluación de riesgos de ISO 27001 Cláusula 6.1.2.
        """)

        st.markdown("**Proceso de gestión de riesgos de IA (6 fases):**")
        for fase in PROCESO_GESTION_RIESGOS_23894:
            with st.expander(f"**{fase['fase']}** (Cláusula {fase['clausula']})"):
                st.markdown(f"{fase['actividades']}")
                st.markdown(f"**Técnicas:** {fase['tecnicas']}")
                st.markdown(f"**Salidas:** {fase['salidas']}")

        st.markdown("---")
        st.markdown("**Catálogo de riesgos de IA (ISO 23894 mapeado a controles 27001/42001):**")

        for riesgo in RIESGOS_IA_23894:
            with st.expander(f"**{riesgo['riesgo']}** — ISO 23894 Cláusula {riesgo['clausula_23894']}"):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"**Descripción:** {riesgo['descripcion']}")
                    st.markdown(f"**📌 Ejemplo en salud:** {riesgo['ejemplo_salud']}")
                with col_b:
                    st.markdown("**Controles ISO 27001 relacionados:**")
                    for c in riesgo['controles_27001']:
                        st.markdown(f"- {c}")
                    st.markdown("**Controles ISO 42001 relacionados:**")
                    for c in riesgo['controles_42001']:
                        st.markdown(f"- {c}")

    with tab_rol[3]:
        st.markdown("### Base de Conocimiento del Auditor")
        st.markdown("""
        La base de conocimiento RAG contiene **documentos normativos oficiales** indexados para consulta.
        El chat auditor puede responder preguntas basadas en estos documentos.
        """)

        import os
        kb_path = "knowledge_base"
        archivos = []
        if os.path.exists(kb_path):
            for f in os.listdir(kb_path):
                if f.endswith(('.pdf', '.txt', '.docx')):
                    archivos.append(f)

        col_docs, col_stats = st.columns(2)
        with col_docs:
            st.markdown("**Documentos en la base:**")
            for a in sorted(archivos):
                st.markdown(f"- 📄 {a}")

        with col_stats:
            from rag_knowledge import base_conocimiento_activa
            if base_conocimiento_activa():
                st.success("✅ Índice FAISS activo — La base RAG está disponible para consultas")
            else:
                st.warning("⚠️ Índice FAISS no encontrado — Ejecuta la indexación desde la pestaña Base RAG")

            with st.expander("💡 ¿Cómo usar la base de conocimiento?"):
                st.markdown("""
                1. Ve a la pestaña **📚 Base RAG** e indexa los documentos
                2. Usa el **💬 Chat Auditor** para hacer preguntas específicas
                3. El chat responderá basado en los documentos indexados
                
                **Ejemplos de consultas:**
                - "¿Qué dice ISO 19011 sobre la competencia del auditor?"
                - "¿Cómo evalúa ISO 23894 el riesgo de deriva del modelo?"
                - "¿Qué controles del Anexo A de ISO 27001 aplican a sistemas de IA?"
                - "¿Cuáles son los principios de auditoría según ISO 19011?"
                """)

    with tab_rol[4]:
        st.markdown("### Competencias del Auditor de IA en IC")
        st.markdown("""
        Basado en ISO 19011 Cláusula 7.2 (Competencia de los auditores) y los requisitos específicos para auditoría de IA.
        """)

        df_comp = [{"Área": c["area"], "Descripción": c["descripcion"],
                     "Nivel requerido": c["nivel_requerido"], "Cómo obtenerlo": c["como_obtenerlo"]}
                   for c in COMPETENCIAS_AUDITOR_IA]
        import pandas as pd
        st.dataframe(
            pd.DataFrame(df_comp),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Área": st.column_config.TextColumn("Área de Competencia", width="medium"),
                "Descripción": st.column_config.TextColumn("Descripción", width="large"),
                "Nivel requerido": st.column_config.TextColumn("Nivel", width="small"),
                "Cómo obtenerlo": st.column_config.TextColumn("Ruta de formación", width="large")
            }
        )

        st.markdown("---")
        st.markdown("**🧭 Ruta de certificación del auditor IA-SEC:**")
        st.markdown("""
        1. Auditor Líder ISO 27001:2022 (5 días)
        2. Curso ISO 19011:2018 — Metodología de auditoría (2 días)
        3. ISO/IEC 42001:2023 — Fundamentos de auditoría de IA (3 días)
        4. ISO/IEC 23894:2023 — Gestión de riesgos de IA (2 días)
        5. Práctica supervisada: 3 auditorías como observador
        6. Certificación como Auditor IA-SEC
        """)


def mostrar_guia_mejorada():
    """Pestaña Guía enriquecida con ISO 27001 como eje + referencias a ISO 19011 e ISO 23894."""
    st.markdown("#### 📋 Diccionario Unificado de Controles IA-SEC")
    st.markdown("**ISO/IEC 27001:2022** + **NIST CSF 2.0** + **ISO/IEC 42001:2023** + **ISO 19011** + **ISO 23894**")
    st.markdown("Base de referencia completa para auditores de ciberseguridad e IA en infraestructuras críticas.")

    import pandas as pd

    marco_seleccionado = st.selectbox(
        "📚 Selecciona el Marco Normativo",
        ["ISO/IEC 27001:2022", "NIST Cybersecurity Framework 2.0", "ISO/IEC 42001:2023", "Vista integrada"],
        help="Selecciona el marco que deseas consultar o 'Vista integrada' para comparación cruzada"
    )

    def obtener_dataset_marco(marco):
        if marco == "ISO/IEC 27001:2022":
            return [
                {"Marco": "ISO 27001", "Dominio": "Organizacional", "Control": "A.5.1", "Nombre": "Políticas de seguridad de la información", "Objetivo": "Aprobación formal, publicación y revisión periódica de políticas de seguridad.", "Relevancia_IC": "Alta", "ISO_19011": "6.2 — Planificación de auditoría", "ISO_23894": "Relacionado — Gobernanza de riesgos"},
                {"Marco": "ISO 27001", "Dominio": "Organizacional", "Control": "A.5.2", "Nombre": "Roles y responsabilidades en seguridad", "Objetivo": "Asignar y comunicar responsabilidades de seguridad.", "Relevancia_IC": "Muy Alta", "ISO_19011": "7.2 — Competencia del auditor", "ISO_23894": "4.1 — Principios de gestión de riesgos"},
                {"Marco": "ISO 27001", "Dominio": "Organizacional", "Control": "A.5.9", "Nombre": "Inventario de información y otros activos", "Objetivo": "Identificar activos, propietarios y ciclo de vida completo.", "Relevancia_IC": "Crítica", "ISO_19011": "6.3 — Preparación", "ISO_23894": "5.2 — Identificación de activos de IA"},
                {"Marco": "ISO 27001", "Dominio": "Organizacional", "Control": "A.5.15", "Nombre": "Control de acceso", "Objetivo": "Establecer reglas basadas en requisitos de negocio y mínimo privilegio.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "6.4 — Seguridad física/funcional"},
                {"Marco": "ISO 27001", "Dominio": "Organizacional", "Control": "A.5.23", "Nombre": "Seguridad en el uso de servicios cloud", "Objetivo": "Definir requisitos de seguridad para adquirir y usar servicios en la nube.", "Relevancia_IC": "Muy Alta", "ISO_19011": "6.3 — Preparación", "ISO_23894": "6.2 — Privacidad"},
                {"Marco": "ISO 27001", "Dominio": "Organizacional", "Control": "A.5.30", "Nombre": "Preparación de las TIC para continuidad", "Objetivo": "Asegurar que las TIC puedan recuperar sus operaciones tras una interrupción.", "Relevancia_IC": "Crítica", "ISO_19011": "6.6 — Seguimiento", "ISO_23894": "6.4 — Seguridad física/funcional"},
                {"Marco": "ISO 27001", "Dominio": "Personas", "Control": "A.6.1", "Nombre": "Investigación de antecedentes", "Objetivo": "Verificar historial de empleados según normativas antes del empleo.", "Relevancia_IC": "Alta", "ISO_19011": "7.2 — Competencia", "ISO_23894": "—"},
                {"Marco": "ISO 27001", "Dominio": "Personas", "Control": "A.6.3", "Nombre": "Concientización y formación en seguridad", "Objetivo": "Capacitar regularmente al personal en políticas de seguridad.", "Relevancia_IC": "Muy Alta", "ISO_19011": "7.2 — Competencia", "ISO_23894": "4.2 — Cultura de riesgos"},
                {"Marco": "ISO 27001", "Dominio": "Físico", "Control": "A.7.1", "Nombre": "Perímetros de seguridad física", "Objetivo": "Proteger áreas sensibles contra acceso no autorizado o daños.", "Relevancia_IC": "Alta", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "—"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.1", "Nombre": "Dispositivos de usuario final", "Objetivo": "Proteger información tratada en laptops, móviles y equipos remotos.", "Relevancia_IC": "Alta", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "—"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.8", "Nombre": "Gestión de vulnerabilidades técnicas", "Objetivo": "Obtener info sobre vulnerabilidades y aplicar parches oportunamente.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "5.5 — Vulnerabilidad adversarial"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.12", "Nombre": "Prevención de fuga de datos (DLP)", "Objetivo": "Aplicar medidas para evitar extracción no autorizada de datos sensibles.", "Relevancia_IC": "Muy Alta", "ISO_19011": "6.5 — Informe", "ISO_23894": "6.2 — Privacidad"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.15", "Nombre": "Registros (Logging)", "Objetivo": "Registrar, guardar y proteger logs de eventos, fallos y accesos.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Evidencia", "ISO_23894": "5.3 — Opacidad algorítmica"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.16", "Nombre": "Monitoreo de actividades", "Objetivo": "Monitorear comportamientos anómalos en sistemas y redes.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "5.4 — Deriva del modelo"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.24", "Nombre": "Uso de criptografía", "Objetivo": "Definir políticas para el uso eficaz del cifrado de datos.", "Relevancia_IC": "Muy Alta", "ISO_19011": "—", "ISO_23894": "6.2 — Privacidad"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.28", "Nombre": "Desarrollo seguro de software", "Objetivo": "Integrar reglas de seguridad en todo el ciclo de vida del software.", "Relevancia_IC": "Muy Alta", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "5.5 — Adversarial"},
            ]
        elif marco == "NIST Cybersecurity Framework 2.0":
            return [
                {"Marco": "NIST CSF 2.0", "Dominio": "IDENTIFY", "Control": "ID.AM-1", "Nombre": "Assets Management", "Objetivo": "Identificar y gestionar activos.", "Relevancia_IC": "Crítica", "ISO_19011": "6.3 — Preparación", "ISO_23894": "5.2 — Identificación"},
                {"Marco": "NIST CSF 2.0", "Dominio": "IDENTIFY", "Control": "ID.RA-1", "Nombre": "Risk Assessment", "Objetivo": "Realizar evaluación de riesgos.", "Relevancia_IC": "Crítica", "ISO_19011": "6.2 — Planificación", "ISO_23894": "6.1 — Evaluación de riesgos"},
                {"Marco": "NIST CSF 2.0", "Dominio": "PROTECT", "Control": "PR.AC-1", "Nombre": "Access Control", "Objetivo": "Implementar control de acceso.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "6.4 — Seguridad"},
                {"Marco": "NIST CSF 2.0", "Dominio": "PROTECT", "Control": "PR.AT-1", "Nombre": "Awareness and Training", "Objetivo": "Proporcionar concientización.", "Relevancia_IC": "Muy Alta", "ISO_19011": "7.2 — Competencia", "ISO_23894": "4.2 — Cultura"},
                {"Marco": "NIST CSF 2.0", "Dominio": "DETECT", "Control": "DE.AE-1", "Nombre": "Anomalous Activity Detection", "Objetivo": "Detectar actividad anómala.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "5.4 — Deriva"},
                {"Marco": "NIST CSF 2.0", "Dominio": "RESPOND", "Control": "RS.RP-1", "Nombre": "Response Planning", "Objetivo": "Desarrollar planes de respuesta.", "Relevancia_IC": "Crítica", "ISO_19011": "6.5 — Informe", "ISO_23894": "6.1.5 — Tratamiento"},
                {"Marco": "NIST CSF 2.0", "Dominio": "RECOVER", "Control": "RC.RP-1", "Nombre": "Recovery Planning", "Objetivo": "Desarrollar planes de recuperación.", "Relevancia_IC": "Crítica", "ISO_19011": "6.6 — Seguimiento", "ISO_23894": "6.2 — Monitoreo"},
            ]
        elif marco == "ISO/IEC 42001:2023":
            return [
                {"Marco": "ISO 42001", "Dominio": "Liderazgo", "Control": "5.1", "Nombre": "Liderazgo y compromiso", "Objetivo": "Demostrar liderazgo con el SGIA.", "Relevancia_IC": "Crítica", "ISO_19011": "6.2 — Iniciación", "ISO_23894": "4 — Principios"},
                {"Marco": "ISO 42001", "Dominio": "Liderazgo", "Control": "5.2", "Nombre": "Política de IA", "Objetivo": "Establecer política de IA.", "Relevancia_IC": "Crítica", "ISO_19011": "6.3 — Preparación", "ISO_23894": "4.1 — Política de riesgos"},
                {"Marco": "ISO 42001", "Dominio": "Planificación", "Control": "6.1", "Nombre": "Acciones para abordar riesgos", "Objetivo": "Planificar acciones para riesgos de IA.", "Relevancia_IC": "Crítica", "ISO_19011": "6.2 — Planificación", "ISO_23894": "6.1 — Proceso completo"},
                {"Marco": "ISO 42001", "Dominio": "Operación", "Control": "8.6", "Nombre": "Monitoreo y medición", "Objetivo": "Monitorear rendimiento de sistemas IA.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "5.4 — Deriva"},
                {"Marco": "ISO 42001", "Dominio": "Controles IA", "Control": "A.2", "Nombre": "Evaluación de impacto", "Objetivo": "Evaluar impacto en partes interesadas.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Hallazgos", "ISO_23894": "6.3 — Impacto social"},
                {"Marco": "ISO 42001", "Dominio": "Controles IA", "Control": "A.5", "Nombre": "Datos para IA", "Objetivo": "Gestionar datos usados en IA.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Evidencia", "ISO_23894": "6.2 — Privacidad"},
                {"Marco": "ISO 42001", "Dominio": "Controles IA", "Control": "A.6", "Nombre": "Monitoreo de sistemas IA", "Objetivo": "Monitorear durante ciclo de vida.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "5.4 — Deriva"},
                {"Marco": "ISO 42001", "Dominio": "Controles IA", "Control": "A.7", "Nombre": "Desarrollo seguro de IA", "Objetivo": "Asegurar desarrollo seguro.", "Relevancia_IC": "Crítica", "ISO_19011": "6.4 — Ejecución", "ISO_23894": "5.5 — Adversarial"},
            ]
        else:
            return obtener_dataset_marco("ISO/IEC 27001:2022") + obtener_dataset_marco("NIST Cybersecurity Framework 2.0") + obtener_dataset_marco("ISO/IEC 42001:2023")

    controles_data = obtener_dataset_marco(marco_seleccionado)

    if marco_seleccionado == "ISO/IEC 27001:2022":
        st.info("📋 **ISO/IEC 27001:2022** — Sistema de Gestión de Seguridad de la Información. Marco fundamental para la gestión integral de la seguridad. Integrado con ISO 19011 (metodología de auditoría) e ISO 23894 (gestión de riesgos de IA).")
    elif marco_seleccionado == "NIST Cybersecurity Framework 2.0":
        st.info("🛡️ **NIST CSF 2.0** — Marco voluntario de ciberseguridad. Especialmente relevante para infraestructuras críticas.")
    elif marco_seleccionado == "ISO/IEC 42001:2023":
        st.info("🤖 **ISO/IEC 42001:2023** — Sistema de Gestión de IA. Primer estándar internacional para gestionar IA de manera responsable, ética y segura.")
    else:
        st.info("🔗 **Vista Integrada** — Comparación completa de los 5 marcos para auditoría unificada de ciberseguridad e IA en infraestructuras críticas.")

    df_controles = pd.DataFrame(controles_data)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Controles", len(controles_data))
    with col2:
        dominios_unicos = len(df_controles['Dominio'].unique()) if 'Dominio' in df_controles.columns else 0
        st.metric("Dominios", dominios_unicos)
    with col3:
        criticos = len(df_controles[df_controles['Relevancia_IC'] == 'Crítica']) if 'Relevancia_IC' in df_controles.columns else 0
        st.metric("Controles Críticos IC", criticos)
    with col4:
        if 'ISO_19011' in df_controles.columns:
            con_19011 = len(df_controles[df_controles['ISO_19011'] != '—'])
            st.metric("Mapeados a ISO 19011", con_19011)

    column_config = {
        "Marco": st.column_config.TextColumn("Marco", width="small"),
        "Dominio": st.column_config.TextColumn("Dominio", width="medium"),
        "Control": st.column_config.TextColumn("Control", width="small"),
        "Nombre": st.column_config.TextColumn("Nombre del Control", width="large"),
        "Objetivo": st.column_config.TextColumn("Objetivo", width="xlarge"),
        "Relevancia_IC": st.column_config.TextColumn("Relevancia IC", width="small"),
    }

    has_19011 = 'ISO_19011' in df_controles.columns
    has_23894 = 'ISO_23894' in df_controles.columns

    if has_19011:
        column_config["ISO_19011"] = st.column_config.TextColumn("ISO 19011\n(Metodología)", width="medium")
    if has_23894:
        column_config["ISO_23894"] = st.column_config.TextColumn("ISO 23894\n(Riesgos IA)", width="medium")

    st.dataframe(
        df_controles,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config=column_config
    )

    if marco_seleccionado != "Vista integrada":
        with st.expander("📖 Información del Marco Normativo"):
            if marco_seleccionado == "ISO/IEC 27001:2022":
                st.markdown("""
                **ISO/IEC 27001:2022** establece los requisitos para un SGSI.

                **Relación con ISO 19011:** La auditoría del SGSI debe seguir las directrices de ISO 19011 para garantizar consistencia, imparcialidad y calidad en los hallazgos.

                **Relación con ISO 23894:** Los riesgos de IA (opacidad, deriva, adversarial, sesgo, privacidad) deben integrarse en el proceso de evaluación de riesgos de ISO 27001 Cláusula 6.1.2.
                """)
            elif marco_seleccionado == "NIST Cybersecurity Framework 2.0":
                st.markdown("""
                **NIST CSF 2.0** proporciona orientación para gestionar riesgos de ciberseguridad.

                **6 funciones principales:** IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER, GOVERN.
                """)
            elif marco_seleccionado == "ISO/IEC 42001:2023":
                st.markdown("""
                **ISO/IEC 42001:2023** especifica requisitos para un AIMS.

                **Relación con ISO 23894:** La gestión de riesgos de IA (Cláusula 6) de ISO 42001 se complementa con la guía detallada de ISO 23894.
                """)
