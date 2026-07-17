from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🛡️ Matriz de Riesgos de Inteligencia Artificial")
    st.markdown("""
    **Feed automatizado de vulnerabilidades IA + Matriz de Riesgos personalizada**
    Consulta en tiempo real: AVID (avidml.org) · MITRE ATLAS (atlas.mitre.org) · MIT AI Risk Repository (airisk.mit.edu)
    """)

    # ── Actualización automática al cargar ───────────────────────────────
    if "feed_inicializado" not in st.session_state:
        st.session_state["feed_inicializado"] = False

    if not st.session_state["feed_inicializado"]:
        with st.spinner("🔄 Verificando base de conocimiento de vulnerabilidades IA..."):
            try:
                from database import stats_vulnerabilidades

                stats = stats_vulnerabilidades()
                ahora = ahora_bogota()
                ultima_act = stats.get("ultima_actualizacion")
                total = stats.get("total", 0)

                necesita_actualizar = total == 0 or total is None
                if not necesita_actualizar and ultima_act:
                    try:
                        ultima_dt = datetime.fromisoformat(ultima_act)
                        if (ahora_bogota() - ultima_dt).total_seconds() > 86400:
                            necesita_actualizar = True
                    except (ValueError, TypeError):
                        necesita_actualizar = True

                if necesita_actualizar:
                    from ingestor.sources import fetch_all as _fetch_all_src
                    raw = _fetch_all_src(limit_per_source=9999, include_nvd=False)
                    if raw:
                        normalized = normalize_batch(raw)
                        for v in normalized:
                            p = v.get('probabilidad_base', 3)
                            s = v.get('severidad_tecnica', 3)
                            riesgo = calcular_riesgo(p, s)
                            v['riesgo_valor'] = riesgo['riesgo_valor']
                            v['nivel_riesgo'] = riesgo['nivel_riesgo']
                            v['criticidad'] = criticidad_compuesta(p, s)
                        insertados, errores = guardar_lote_vulnerabilidades(normalized)
                        limpiar_vulnerabilidades_antiguas(dias=90)
                        exportar_excel_respaldo()
                        st.success(f"✅ Base actualizada: {insertados} nuevas vulnerabilidades")
                else:
                    st.info(f"📊 Base de datos actual: {int(total or 0)} vulnerabilidades")
            except Exception as e:
                st.warning(f"⚠️ No se pudo actualizar automáticamente: {e}")
        st.session_state["feed_inicializado"] = True

    # ── Panel de control de actualización ────────────────────────────────
    with st.expander("⚙️ **Panel de control del feed**", expanded=False):
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)

        with col_s1:
            if st.button("🔄 Actualizar ahora", key="btn_feed_now", type="primary"):
                st.session_state["forzar_actualizacion"] = True

        with col_s2:
            intervalo = st.selectbox(
                "Actualización automática",
                ["Manual", "Cada 1 hora", "Cada 6 horas", "Cada 12 horas", "Cada 24 horas"],
                index=3,
                key="intervalo_feed",
            )

        with col_s3:
            incluir_nvd = st.checkbox("Incluir NVD (CVEs de IA)", value=False, key="feed_nvd")

        with col_s4:
            proveedor_normalizador = st.selectbox(
                "Proveedor IA",
                ["deepseek", "google"],
                index=0,
                key="feed_proveedor",
            )
            modelo_normalizador = st.selectbox(
                "Modelo",
                MODEL_MAP.get(proveedor_normalizador, ["deepseek-chat"]),
                key="feed_modelo",
            )

        # Última actualización
        try:
            from database import stats_vulnerabilidades
            sv = stats_vulnerabilidades()
            ult = sv.get("ultima_actualizacion", "Nunca")
            if ult and ult != "Nunca":
                st.caption(f"📅 Última actualización: {ult[:19].replace('T', ' ')} UTC")
        except Exception:
            st.caption("📅 Última actualización: Desconocida")

    # ── Forzar actualización ─────────────────────────────────────────────
    if st.session_state.get("forzar_actualizacion", False):
        st.session_state["forzar_actualizacion"] = False
        with st.spinner("🔄 Consultando MITRE ATLAS, AVID, MIT AI Risk Repository..."):
            try:
                from ingestor.sources import fetch_all as _fetch_all_src
                raw = _fetch_all_src(limit_per_source=9999, include_nvd=incluir_nvd)
                if not raw:
                    st.error("No se obtuvieron datos de las fuentes.")
                else:
                    proveedor = st.session_state.get("feed_proveedor", "deepseek")
                    modelo = st.session_state.get("feed_modelo", "deepseek-chat")
                    set_provider(proveedor, modelo)

                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    normalized = []
                    for idx, report in enumerate(raw):
                        status_text.text(f"Normalizando {idx+1}/{len(raw)}: {report.get('id', report.get('title',''))[:60]}...")
                        result = analizar_vulnerabilidad(report.get("source", "DESCONOCIDA"), report)
                        normalized.append(result)
                        progress_bar.progress((idx + 1) / len(raw))
                    progress_bar.empty()
                    status_text.empty()

                    for v in normalized:
                        p = v.get('probabilidad_base', 3)
                        s = v.get('severidad_tecnica', 3)
                        riesgo = calcular_riesgo(p, s)
                        v['riesgo_valor'] = riesgo['riesgo_valor']
                        v['nivel_riesgo'] = riesgo['nivel_riesgo']
                        v['criticidad'] = criticidad_compuesta(p, s)

                    insertados, errores = guardar_lote_vulnerabilidades(normalized)
                    limpiadas = limpiar_vulnerabilidades_antiguas(dias=90)
                    ruta_excel = exportar_excel_respaldo()

                    st.session_state["ultimas_vulns"] = normalized
                    st.session_state["vuln_stats"] = resumen_estadistico(normalized)

                    # ── definir msgs ANTES de usarlo ──
                    msgs = []
                    if insertados > 0:
                        msgs.append(f"✅ {insertados} vulnerabilidades nuevas insertadas")
                    if errores > 0:
                        msgs.append(f"⚠️ {errores} duplicados ignorados")
                    if limpiadas > 0:
                        msgs.append(f"🗑️ {limpiadas} vulnerabilidades antiguas desactivadas")
                    if ruta_excel:
                        msgs.append(f"📁 Excel respaldo generado")
                    st.success(" | ".join(msgs) if msgs else "✅ Base de datos actualizada")
                    st.rerun()
            except Exception as e:
                st.error(f"Error durante la actualización: {e}")
                st.code(traceback.format_exc())

    # ── Paso 1: Cuestionario contextual ────────────────────────────────────
    with st.expander("📋 **Paso 1: Contexto de la organización** (completar una vez)", expanded="contexto_ok" not in st.session_state):
        st.markdown("Responde estas preguntas para personalizar la matriz de riesgos:")

        respuestas = {}
        cols_preg = st.columns(2)
        for i, q in enumerate(CUESTIONARIO_CONTEXTO):
            with cols_preg[i % 2]:
                key = f"ctx_{q['id']}"
                if q["tipo"] == "select":
                    respuestas[q["id"]] = st.selectbox(
                        q["pregunta"],
                        q["opciones"],
                        index=0,
                        key=key,
                    )
                elif q["tipo"] == "multiselect":
                    respuestas[q["id"]] = st.multiselect(
                        q["pregunta"],
                        q["opciones"],
                        key=key,
                    )

        col_ctx1, col_ctx2 = st.columns([1, 4])
        with col_ctx1:
            if st.button("✅ Guardar Contexto", key="btn_guardar_ctx", type="primary"):
                st.session_state["contexto_ok"] = True
                st.session_state["respuestas_contexto"] = respuestas
                st.session_state["prompt_contexto"] = generar_prompt_contexto(respuestas)
                st.rerun()
        with col_ctx2:
            if "contexto_ok" in st.session_state:
                st.success("✅ Contexto guardado. Ve al Paso 2.")

    # ── Paso 2: Consultar y normalizar fuentes ────────────────────────────
    if "contexto_ok" in st.session_state:
        paso2_expanded = "datos_cargados" not in st.session_state
        with st.expander("🔍 **Paso 2: Consultar fuentes de vulnerabilidades**", expanded=paso2_expanded):
            col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
            with col_f1:
                limit_per_source = st.number_input("Vulnerabilidades por fuente", min_value=1, max_value=20, value=5, key="vuln_limit")
            with col_f2:
                incluir_nvd = st.checkbox("Incluir NVD (CVEs de IA)", value=False, key="vuln_nvd")
            with col_f3:
                usar_deepseek = st.checkbox("Usar DeepSeek para normalización", value=True, key="vuln_ds")

            if st.button("🚀 Consultar y Normalizar Fuentes", key="btn_fetch_all", type="primary"):
                with st.spinner("Consultando AVID, MITRE ATLAS, MIT AI Risk Repository..."):
                    from ingestor.sources import fetch_all as _fetch_all_src
                    raw_reports = _fetch_all_src(limit_per_source=limit_per_source, include_nvd=incluir_nvd)
                st.info(f"📥 {len(raw_reports)} reportes obtenidos de las fuentes.")

                progress_bar = st.progress(0)
                status_text = st.empty()
                normalized = []
                proveedor = st.session_state.get("feed_proveedor", "deepseek")
                modelo = st.session_state.get("feed_modelo", "deepseek-chat")
                set_provider(proveedor, modelo)
                for idx, report in enumerate(raw_reports):
                    fuente = report.get("source", "DESCONOCIDA")
                    status_text.text(f"Normalizando {idx+1}/{len(raw_reports)}: {report.get('id', report.get('title', ''))[:60]}...")
                    result = analizar_vulnerabilidad(fuente, report)
                    normalized.append(result)
                    progress_bar.progress((idx + 1) / len(raw_reports))
                progress_bar.empty()
                status_text.empty()
                st.success(f"✅ {len(normalized)} vulnerabilidades normalizadas.")

                for v in normalized:
                    p = v.get("probabilidad_base", 3)
                    s = v.get("severidad_tecnica", 3)
                    riesgo = calcular_riesgo(p, s)
                    v["riesgo_valor"] = riesgo["riesgo_valor"]
                    v["nivel_riesgo"] = riesgo["nivel_riesgo"]
                    v["criticidad"] = criticidad_compuesta(p, s)
                    if "contexto_org" not in v and "prompt_contexto" in st.session_state:
                        v["contexto_org"] = st.session_state["prompt_contexto"]

                insertados, errores = guardar_lote_vulnerabilidades(normalized)
                st.session_state["ultimas_vulns"] = normalized
                st.session_state["vuln_stats"] = resumen_estadistico(normalized)

                if errores > 0:
                    st.warning(f"⚠️ {insertados} insertadas, {errores} con errores (posibles duplicados)")
                else:
                    st.success(f"✅ {insertados} vulnerabilidades guardadas en base de datos.")
                st.session_state["datos_cargados"] = True
                st.rerun()

        # ── Botón para re-consultar fuera del expander ──
        if "datos_cargados" in st.session_state:
            col_re1, _ = st.columns([1, 4])
            with col_re1:
                if st.button("🔄 Re-consultar fuentes", key="btn_refetch", type="secondary"):
                    st.session_state.pop("datos_cargados", None)
                    st.rerun()
    else:
        st.info("⬅️ Completa el **Paso 1** (Contexto de la organización) para habilitar la consulta de fuentes.")

    # ── Paso 3: Visualizar resultados ─────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📊 Vulnerabilidades Activas")

    vulns = st.session_state.get("ultimas_vulns", None)
    if vulns is None:
        vulns = listar_vulnerabilidades(limit=9999)

    if not vulns:
        st.info("Aún no hay vulnerabilidades consultadas. Ejecuta el Paso 2 para poblar la matriz.")
    else:
        stats_v = st.session_state.get("vuln_stats", resumen_estadistico(vulns))

        # Métricas rápidas
        mcols = st.columns(6)
        with mcols[0]:
            st.metric("Total", stats_v["total"])
        with mcols[1]:
            st.metric("🔴 Extremos", stats_v["por_nivel"].get("EXTREMO", 0))
        with mcols[2]:
            st.metric("🟠 Altos", stats_v["por_nivel"].get("ALTO", 0))
        with mcols[3]:
            st.metric("🟡 Medios", stats_v["por_nivel"].get("MEDIO", 0))
        with mcols[4]:
            st.metric("🟢 Bajos", stats_v["por_nivel"].get("BAJO", 0))
        with mcols[5]:
            st.metric("Criticidad Prom.", f"{stats_v['criticidad_promedio']}%")

        # --- B --- BÚSQUEDA Y FILTROS ---
        with st.expander("🔎 **Filtrar vulnerabilidades**", expanded=False):
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                search_text = st.text_input("🔍 Buscar en resumen", placeholder="ej. inyección, privacidad...", key="vuln_search")
            with col_f2:
                fuentes_unicas = sorted(set(v.get("fuente_origen", "") for v in vulns))
                fuentes_sel = st.multiselect("Fuente", fuentes_unicas, key="vuln_fuente")
            with col_f3:
                tipos_unicos = sorted(set(v.get("clasificacion_tipo", "") for v in vulns))
                tipos_sel = st.multiselect("Tipo", tipos_unicos, key="vuln_tipo")
            with col_f4:
                niveles_unicos = ["EXTREMO", "ALTO", "MEDIO", "BAJO"]
                niveles_sel = st.multiselect("Nivel de riesgo", niveles_unicos, key="vuln_nivel")

        # Aplicar filtros
        vulns_filtradas = vulns.copy()
        if search_text:
            stx = search_text.lower()
            vulns_filtradas = [v for v in vulns_filtradas if stx in v.get("resumen_es", "").lower() or stx in v.get("id_vulnerabilidad", "").lower()]
        if fuentes_sel:
            vulns_filtradas = [v for v in vulns_filtradas if v.get("fuente_origen", "") in fuentes_sel]
        if tipos_sel:
            vulns_filtradas = [v for v in vulns_filtradas if v.get("clasificacion_tipo", "") in tipos_sel]
        if niveles_sel:
            vulns_filtradas = [v for v in vulns_filtradas if v.get("nivel_riesgo", "") in niveles_sel]

        # --- C --- PAGINACIÓN ---
        ITEMS_POR_PAGINA = 25
        total_items = len(vulns_filtradas)
        total_paginas = max(1, (total_items + ITEMS_POR_PAGINA - 1) // ITEMS_POR_PAGINA)
        pagina_actual = st.session_state.get("vuln_pagina", 1)
        if pagina_actual > total_paginas:
            pagina_actual = 1
            st.session_state["vuln_pagina"] = 1

        inicio = (pagina_actual - 1) * ITEMS_POR_PAGINA
        fin = min(inicio + ITEMS_POR_PAGINA, total_items)
        vulns_pagina = vulns_filtradas[inicio:fin]

        # Tabla de vulnerabilidades
        df_vulns = []
        for v in vulns_pagina:
            df_vulns.append({
                "ID": v.get("id_vulnerabilidad", ""),
                "Fuente": v.get("fuente_origen", ""),
                "Resumen (ES)": v.get("resumen_es", "")[:120],
                "Táctica MITRE": v.get("tactica_mitre", ""),
                "Tipo": v.get("clasificacion_tipo", ""),
                "Prob": v.get("probabilidad_base", 3),
                "Sev": v.get("severidad_tecnica", 3),
                "Riesgo": v.get("riesgo_valor", 9),
                "Nivel": v.get("nivel_riesgo", "MEDIO"),
            })

        df = pd.DataFrame(df_vulns)

        # Color por nivel de riesgo
        def color_nivel(val):
            colors = {"EXTREMO": "background-color: #FF0000; color: white",
                      "ALTO": "background-color: #FF6600; color: black",
                      "MEDIO": "background-color: #FFD700; color: black",
                      "BAJO": "background-color: #92D050; color: black"}
            return colors.get(val, "")

        styled_df = df.style.map(color_nivel, subset=["Nivel"])
        st.dataframe(styled_df, use_container_width=True, hide_index=True,
                     column_config={
                         "Riesgo": st.column_config.NumberColumn(format="%d"),
                         "Prob": st.column_config.NumberColumn(format="%d"),
                         "Sev": st.column_config.NumberColumn(format="%d"),
                     })

        # Navegación de páginas
        if total_paginas > 1:
            col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([2, 1, 2, 1, 2])
            with col_p1:
                if st.button("◀ Anterior", key="vuln_prev", disabled=(pagina_actual <= 1), use_container_width=True):
                    st.session_state["vuln_pagina"] = max(1, pagina_actual - 1)
                    st.rerun()
            with col_p2:
                st.markdown(f"<p style='text-align:center;padding-top:8px;color:#8a8f98;font-size:0.85rem;'>{inicio+1}–{fin} de {total_items}</p>", unsafe_allow_html=True)
            with col_p3:
                st.markdown(f"<p style='text-align:center;padding-top:8px;color:#8a8f98;font-size:0.85rem;'>Pág. {pagina_actual}/{total_paginas}</p>", unsafe_allow_html=True)
            with col_p4:
                salto = st.number_input("Ir a pág.", min_value=1, max_value=total_paginas, value=pagina_actual, key="vuln_ir_pag", label_visibility="collapsed")
            with col_p5:
                if st.button("Siguiente ▶", key="vuln_next", disabled=(pagina_actual >= total_paginas), use_container_width=True):
                    st.session_state["vuln_pagina"] = min(total_paginas, pagina_actual + 1)

        # ── Expandir detalle de cada vulnerabilidad ──
        with st.expander("🔬 Ver detalle completo de vulnerabilidades"):
            for v in vulns:
                nivel = v.get("nivel_riesgo", "MEDIO")
                emoji = {"EXTREMO": "🔴", "ALTO": "🟠", "MEDIO": "🟡", "BAJO": "🟢"}
                with st.container():
                    st.markdown(f"""**{emoji.get(nivel, '⚪')} {v.get('id_vulnerabilidad', 'N/A')}** — *{v.get('fuente_origen', '?')}*
    - **Resumen (ES):** {v.get('resumen_es', 'N/A')}
    - **Causa Raíz:** {v.get('causa_raiz', 'N/A')}
    - **Remediación:** {v.get('accion_remediacion', 'N/A')}
    - **Táctica MITRE:** {v.get('tactica_mitre', 'N/A')} → {clasificar_tactica(v.get('tactica_mitre', ''))}
    - **Probabilidad:** {v.get('probabilidad_base', '?')}/5 | **Severidad:** {v.get('severidad_tecnica', '?')}/5 | **Riesgo:** {v.get('riesgo_valor', '?')}/25
    - **Normas:** {', '.join(v.get('normas_aplicables', [])) if isinstance(v.get('normas_aplicables'), list) else v.get('normas_aplicables', 'N/A')}
    """)
                    st.markdown("---")

        # ── Gráficos ──
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("**Distribución por nivel de riesgo**")
            niveles_data = stats_v["por_nivel"]
            fig_niveles = go.Figure(data=[
                go.Pie(
                    labels=list(niveles_data.keys()),
                    values=list(niveles_data.values()),
                    marker_colors=["#FF0000", "#FF6600", "#FFD700", "#92D050"],
                    hole=0.4,
                )
            ])
            fig_niveles.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="white", height=300, showlegend=True,
            )
            st.plotly_chart(fig_niveles, use_container_width=True)

        with col_g2:
            st.markdown("**Distribución por clasificación**")
            clasif_data = stats_v["por_clasificacion"]
            if clasif_data:
                fig_clasif = go.Figure(data=[
                    go.Bar(
                        x=list(clasif_data.keys()),
                        y=list(clasif_data.values()),
                        marker_color="#a78bfa",
                    )
                ])
                fig_clasif.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white", height=300,
                )
                st.plotly_chart(fig_clasif, use_container_width=True)

        # ── Exportar Excel ───────────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 📥 Exportar Matriz de Riesgos IA")

        col_e1, col_e2 = st.columns([1, 3])
        with col_e1:
            if st.button("📊 Generar Excel Matriz de Riesgos", key="btn_export_excel", type="primary"):
                with st.spinner("Generando Excel profesional..."):
                    contexto = st.session_state.get("prompt_contexto", "")
                    excel_bytes = exportar_matriz_riesgos_ia(
                        vulns,
                        contexto_organizacion=contexto,
                        respuestas_cuestionario=st.session_state.get("respuestas_contexto"),
                    )
                    st.session_state["excel_riesgos_ia"] = excel_bytes
                st.success("✅ Excel generado. Descárgalo abajo.")

        if "excel_riesgos_ia" in st.session_state:
            with col_e2:
                st.download_button(
                    "⬇️ Descargar Matriz de Riesgos IA (Excel)",
                    data=st.session_state["excel_riesgos_ia"],
                    file_name=f"Matriz_Riesgos_IA_{ahora_bogota().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_excel_riesgos",
                )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Threat Intelligence — Ransomware Live ────────────────────────────
