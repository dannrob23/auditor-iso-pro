from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🧩 Matriz de Confluencia Normativa IA-SEC")
    st.markdown("**Herramienta de apoyo al auditor** — ISO/IEC 27001:2022 + ISO/IEC 42001:2023 + NIST AI RMF 1.0")
    st.markdown("*23 controles correlacionados · 9 dimensiones operativas · Escala MSPI 6 niveles*")

    # Selección de sector
    sectores_opciones = ["Selecciona un sector..."] + [f"{k}: {v['nombre']}" for k, v in SECTORES_IC.items()]
    sector_seleccionado = st.selectbox(
        "🏭 Sector de Infraestructura Crítica",
        sectores_opciones,
        help="Selecciona el sector específico para contextualizar la evaluación"
    )

    sector_id = None
    if sector_seleccionado != "Selecciona un sector...":
        sector_id = sector_seleccionado.split(":")[0]
        sector_info = obtener_sector(sector_id)
        if sector_info:
            st.info(f"**{sector_info['nombre']}**: {sector_info['descripcion']}")
            st.write(f"**Regulaciones adicionales:** {', '.join(sector_info['regulaciones_adicionales'])}")

    st.markdown("---")

    # Inicializar DataFrame en sesión si no existe
    if 'df_interop' not in st.session_state:
        st.session_state.df_interop = generar_df_interoperabilidad()

    # Mostrar métricas de resumen
    resumen = generar_resumen_interoperabilidad()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Controles", resumen["total_controles"])
    with col2:
        st.metric("Controles Críticos", resumen["por_relevancia"]["Crítica"])
    
    # Calcular cumplimiento actual desde el DataFrame
    df_eval = st.session_state.df_interop
    df_eval['%'] = df_eval['Estado Actual'].apply(calcular_cumplimiento)
    avance_global = df_eval['%'].mean()
    
    with col3:
        st.metric("Dimensiones", len(resumen["dimensiones"]))
    with col4:
        st.metric("Avance Global", f"{avance_global:.1%}")

    st.markdown("---")

    # Editor de datos interactivo (Modo GRC Excel)
    st.markdown("#### 📊 Matriz de Evaluación GRC (Interactivo)")
    st.info("Utiliza esta tabla para evaluar el estado de implementación. Los cambios se guardan automáticamente en la sesión.")
    
    edited_df = st.data_editor(
        st.session_state.df_interop,
        column_config={
            "ID": st.column_config.TextColumn("ID", width="small", disabled=True),
            "Dimensión": st.column_config.TextColumn("Dimensión", width="medium", disabled=True),
            "ISO 27001": st.column_config.TextColumn("ISO 27001", width="medium", disabled=True),
            "ISO 42001": st.column_config.TextColumn("ISO 42001", width="medium", disabled=True),
            "NIST AI RMF": st.column_config.TextColumn("NIST AI RMF", width="medium", disabled=True),
            "Relevancia IC": st.column_config.TextColumn("Relevancia IC", width="small", disabled=True),
            "Estado Actual": st.column_config.SelectboxColumn(
                "Estado Actual",
                options=[
                    "No iniciado", 
                    "En proceso inicial", 
                    "Implementado parcialmente", 
                    "Mayormente implementado", 
                    "Cumplimiento total",
                    "No evaluado"
                ],
                required=True,
                width="medium"
            ),
            "Plan de Acción": st.column_config.TextColumn(
                "¿Qué voy a hacer para lograrlo?",
                width="large"
            )
        },
        hide_index=True,
        use_container_width=True,
        key="grc_editor"
    )
    
    # Actualizar sesión con los cambios
    st.session_state.df_interop = edited_df

    # Botón para descargar en Excel (Estilo GRC GAP)
    if 'df_interop' in st.session_state:
        excel_bytes = exportar_matriz_excel(st.session_state.df_interop)
        st.download_button(
            label="📥 Descargar Matriz de Cumplimiento GRC (Excel)",
            data=excel_bytes,
            file_name="Matriz_Cumplimiento_Integrada_GRC.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Descarga un reporte Excel profesional con pestañas separadas por norma, semáforos de cumplimiento y la tabla de valoración de madurez."
        )

    st.markdown("---")

    # Navegación por dimensiones para vista detallada
    dimensiones = obtener_dimensiones()
    dimension_seleccionada = st.selectbox(
        "🔍 Explorar Requisitos Detallados por Dimensión",
        ["Vista general"] + dimensiones,
        help="Selecciona una dimensión para ver los controles detallados y requisitos específicos de IC"
    )

    if dimension_seleccionada == "Vista general":
        # Vista general con estadísticas
        import pandas as pd

        # Crear tabla resumen por dimensión
        data_dimensiones = []
        for dim in dimensiones:
            controles = obtener_controles_por_dimension(dim)
            criticos = sum(1 for c in controles if c.relevancia_ic == "Crítica")
            muy_altos = sum(1 for c in controles if c.relevancia_ic == "Muy Alta")
            altos = sum(1 for c in controles if c.relevancia_ic == "Alta")
            data_dimensiones.append({
                "Dimensión": dim,
                "Total Controles": len(controles),
                "Críticos": criticos,
                "Muy Altos": muy_altos,
                "Altos": altos
            })

        df_dimensiones = pd.DataFrame(data_dimensiones)
        st.dataframe(df_dimensiones, use_container_width=True, hide_index=True)

        # Gráfico de distribución por relevancia
        fig_relevancia = go.Figure()
        relevancia_data = resumen["por_relevancia"]
        fig_relevancia.add_trace(go.Pie(
            labels=list(relevancia_data.keys()),
            values=list(relevancia_data.values()),
            marker_colors=["#dc2626", "#d97706", "#059669"],
            title="Distribución por relevancia en IC"
        ))
        fig_relevancia.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", showlegend=True,
            height=300,
        )
        st.plotly_chart(fig_relevancia, use_container_width=True)

        # Gráfico de barras de cumplimiento
        # Recalcular cobertura para el gráfico
        evals_dict = {row['ID']: row['Estado Actual'] for _, row in st.session_state.df_interop.iterrows()}
        cobertura = calcular_cobertura(evals_dict)

        st.markdown("#### 📈 Nivel de Cumplimiento por Dimensión")
        cols_cob = st.columns(len(cobertura))
        for i, (dim, stats) in enumerate(cobertura.items()):
            with cols_cob[i % len(cols_cob)]:
                st.metric(dim, f"{stats['porcentaje']}%")
        
        fig_cumplimiento = px.bar(
            x=list(cobertura.keys()),
            y=[s["porcentaje"] for s in cobertura.values()],
            labels={"x": "Dimensión", "y": "% Cumplimiento"},
            title="Porcentaje de Cumplimiento Acumulado",
            color_discrete_sequence=["#a78bfa"]
        )
        fig_cumplimiento.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", height=350
        )
        st.plotly_chart(fig_cumplimiento, use_container_width=True)

    else:
        # Vista detallada de una dimensión
        controles = obtener_controles_por_dimension(dimension_seleccionada)
        st.subheader(f"📋 {dimension_seleccionada}")

        # Controles en formato expandible
        for control in controles:
            relevancia_color = {
                "Crítica": "#dc2626",
                "Muy Alta": "#d97706",
                "Alta": "#059669"
            }.get(control.relevancia_ic, "#64748b")

            with st.expander(f"🔴 {control.id}: {control.iso_27001_ref} ({control.relevancia_ic})"):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("**ISO/IEC 27001:2022**")
                    st.write(f"*{control.iso_27001_ref}*")
                    st.write(control.iso_27001_desc)

                    st.markdown("**ISO/IEC 42001:2023**")
                    st.write(f"*{control.iso_42001_ref}*")
                    st.write(control.iso_42001_desc)

                    st.markdown("**NIST AI RMF 1.0**")
                    st.write(f"*{control.nist_ai_rmf_ref}*")
                    st.write(control.nist_ai_rmf_desc)

                with col_b:
                    st.markdown(f"**Relevancia en IC:** <span style='color:{relevancia_color};font-weight:bold'>{control.relevancia_ic}</span>", unsafe_allow_html=True)
                    st.write("**Requisito específico IC:**")
                    st.write(control.requisito_ic)
                    
                    # Mostrar estado y plan desde la matriz GRC
                    row = st.session_state.df_interop[st.session_state.df_interop['ID'] == control.id]
                    if not row.empty:
                        estado = row['Estado Actual'].values[0]
                        plan = row['Plan de Acción'].values[0]
                        st.markdown(f"**Estado Evaluación:** `{estado}`")
                        if plan:
                            st.success(f"📌 **Plan:** {plan}")

                    st.write("**Riesgo sin control:**")
                    st.write(control.riesgo_sin_control)

    st.markdown("---")

    # Generación de propuestas
    if sector_id:
        st.markdown("### 🎯 Generar Propuesta de Implementación")
        st.markdown("""
        **Metodología:**  
        🔷 **ISO 19011:2018** — Las 5 fases del ciclo de auditoría guían la estructura de la propuesta  
        🔷 **ISO 23894:2023** — Los riesgos de IA (opacidad, deriva, adversarial, sesgo, privacidad, impacto social, seguridad física) se incorporan como catálogo de riesgos  
        🔷 **ISO 27001 + ISO 42001 + NIST AI RMF** — Controles correlacionados para la evaluación
        """)

        # Evaluación de controles
        st.markdown("#### 📝 Datos para la propuesta")
        st.info("La propuesta se basará en los datos ingresados en la Matriz de Evaluación GRC y el contexto organizacional.")

        # Recolectar evaluaciones del DataFrame de la sesión
        controles_evaluados = {row['ID']: row['Estado Actual'] for _, row in st.session_state.df_interop.iterrows()}

        # Contexto organizacional
        contexto_org = st.text_area(
            "📋 Contexto de la organización",
            placeholder="Describe brevemente la organización: tamaño, madurez en ciberseguridad, experiencia previa con IA, regulaciones aplicables, etc.",
            height=100
        )

        # Botón de generación
        if st.button("🚀 Generar Propuesta de Implementación", type="primary"):
            if not contexto_org.strip():
                st.error("Debes proporcionar contexto organizacional.")
            else:
                log_event("INTEROP_PROPOSAL_START", user=usuario, detail=f"Sector: {sector_id} | Controles evaluados: {len(controles_evaluados)}")

                with st.spinner("🤖 Generando propuesta personalizada... esto puede tardar 1-2 minutos."):
                    propuesta = generar_propuesta_ic(
                        sector_id, controles_evaluados, contexto_org,
                        proveedor, modelo, temperatura
                    )

                if propuesta.startswith("ERROR:"):
                    st.error(propuesta)
                else:
                    log_event("INTEROP_PROPOSAL_DONE", user=usuario, result="success", detail=f"Sector: {sector_id} | Propuesta generada")

                    st.success("✅ Propuesta generada exitosamente")

                    # Mostrar propuesta
                    st.markdown("---")
                    st.markdown("## 📄 Propuesta de Implementación")
                    st.markdown(propuesta)

                    # Opciones de descarga
                    col_md, col_pdf = st.columns(2)
                    with col_md:
                        st.download_button(
                            "⬇️ Descargar (.md)",
                            data=propuesta,
                            file_name=f"propuesta_interoperabilidad_{sector_id}.md",
                            mime="text/markdown",
                            key="download_md"
                        )
                    with col_pdf:
                        # Usar función especializada para propuestas de interoperabilidad
                        sector_info = obtener_sector(sector_id)
                        sector_nombre = sector_info["nombre"] if sector_info else sector_id
                        pdf_bytes = generar_pdf_propuesta_interoperabilidad(
                            propuesta, sector_id, sector_nombre, controles_evaluados,
                            usuario, proveedor, modelo
                        )
                        st.download_button(
                            "📄 Descargar PDF (auditoría ISO 19011)",
                            data=pdf_bytes,
                            file_name=f"informe_auditoria_{sector_id}.pdf",
                            mime="application/pdf",
                            key="download_pdf"
                        )

    # Descarga de la matriz completa
    st.markdown("---")
    st.markdown("### 📥 Descargas")
    col_a, col_b = st.columns(2)
    with col_a:
        matriz_md = generar_markdown_matriz(sector_id)
        st.download_button(
            "⬇️ Matriz Interoperabilidad (.md)",
            data=matriz_md,
            file_name=f"matriz_interoperabilidad{'_' + sector_id if sector_id else ''}.md",
            mime="text/markdown",
            key="matriz_md"
        )
    with col_b:
        st.info("💡 **Uso recomendado:** Comparte esta matriz con equipos técnicos para evaluar brechas antes de generar propuestas específicas.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Guía (Enriquecida con ISO 19011 e ISO 23894) ────────────────────────
