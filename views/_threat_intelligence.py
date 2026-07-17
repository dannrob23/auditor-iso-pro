from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🔴 Threat Intelligence — Ransomware Live")
    st.markdown("""
    **Alimenta tu matriz de riesgos con ataques reales.**  
    Cada víctima de ransomware se traduce a un riesgo en formato ISO 27001 5x5,
    con los controles **ISO 27002:2022** que la habrían evitado.
    
    Fuente: [ransomware.live](https://www.ransomware.live/) — 29.520+ víctimas documentadas, 357 grupos rastreados.
    """)
    
    # ── Stats rápidos ──
    try:
        from ingestor.ransomware_feed import consultar_estadisticas as ce
        stats = ce()
        if stats:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🌍 Víctimas totales", f"{stats.get('victims',0):,}")
            c2.metric("👥 Grupos activos", stats.get('groups',0))
            c3.metric("📰 Cobertura prensa", stats.get('press',0))
            c4.metric("🕐 Última actualización", "Hoy")
    except:
        pass
    
    st.markdown("---")
    
    # ── Filtros ──
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        solo_co = st.checkbox("🇨🇴 Solo Colombia", value=True, key="ransom_co")
    with col_f2:
        sectores_opts = ["Todos", "Servicios Financieros", "Salud", "Manufactura",
                         "Tecnología", "Gobierno", "Energía", "Comercio", "Educación",
                         "Transporte", "Legal", "Construcción", "Agricultura y Alimentos"]
        sector_filtro = st.selectbox("Sector", sectores_opts, key="ransom_sector")
    with col_f3:
        grupo_buscar = st.text_input("Grupo específico (opcional)", placeholder="qilin, lockbit...", key="ransom_grupo")
    with col_f4:
        cantidad = st.number_input("Resultados", 1, 50, 10, key="ransom_cant")
    
    # ── Botón consultar ──
    if st.button("🔄 Consultar amenazas actuales", type="primary", use_container_width=True):
        with st.spinner("🔍 Consultando ransomware.live..."):
            import ingestor.ransomware_feed as rf
            
            if grupo_buscar:
                info_grupo = rf.consultar_grupo(grupo_buscar)
                if info_grupo:
                    st.success(f"✅ Inteligencia del grupo **{grupo_buscar}** obtenida")
                    with st.expander("📋 Detalles del grupo", expanded=True):
                        st.json(info_grupo)
                else:
                    st.warning(f"No se encontró información para el grupo '{grupo_buscar}'")
            
            mapa_sectores = {
                "Servicios Financieros": "Financial Services",
                "Salud": "Healthcare", "Manufactura": "Manufacturing",
                "Tecnología": "Technology", "Gobierno": "Government",
                "Energía": "Energy", "Comercio": "Retail", "Educación": "Education",
                "Transporte": "Transportation", "Legal": "Legal",
                "Construcción": "Construction", "Agricultura y Alimentos": "Agriculture and Food Production",
            }
            sector_api = mapa_sectores.get(sector_filtro, sector_filtro)
            
            if solo_co and sector_api and sector_filtro != "Todos":
                # Ambos filtros: país + sector (usar consultar_por_pais y filtrar por sector en la API)
                # La API soporta múltiples filtros: /victims/?country=CO&sector=Healthcare
                import urllib.parse
                url = f"{rf.API_BASE}/victims/?country=CO&sector={urllib.parse.quote(sector_api)}"
                req = urllib.request.Request(url, headers=rf.API_HEADERS)
                try:
                    resp = urllib.request.urlopen(req, timeout=15)
                    data = json.loads(resp.read().decode())
                    victimas = data.get("victims", [])
                    ataques = []
                    for item in victimas[:cantidad]:
                        ataques.append({
                            "grupo": item.get("group", "Desconocido"),
                            "victima": item.get("victim", ""),
                            "pais": "CO",
                            "sector": item.get("activity", "N/A"),
                            "fecha": item.get("discovered", "")[:10],
                            "website": item.get("website", ""),
                            "data_size": str(item.get("data_size") or ""),
                            "descripcion": item.get("description", "")[:200],
                        })
                except:
                    ataques = []
            elif solo_co:
                ataques = rf.consultar_por_pais("CO", cantidad)
            elif sector_filtro != "Todos" and sector_api:
                ataques = rf.consultar_por_sector(sector_api, cantidad)
            else:
                ataques = rf.consultar_victimas_recientes(cantidad)
            
            if not ataques:
                st.info("No se encontraron víctimas con esos filtros.")
            else:
                solo_sector = None if sector_filtro == "Todos" else sector_api
                riesgos = rf.generar_matriz_riesgos(ataques, solo_colombia=False, solo_sector=solo_sector)
                st.session_state["riesgos_ransom"] = riesgos
                st.session_state["sector_filtro_ransom"] = sector_filtro
                st.session_state["controles_ransom"] = rf.sugerir_controles_prioritarios(
                    sector_api if sector_filtro != "Todos" else "Financial Services"
                )
                st.rerun()
    
    # ── Mostrar resultados si hay datos en sesión ──
    if "riesgos_ransom" in st.session_state:
        riesgos = st.session_state["riesgos_ransom"]
        sector_filtro_mostrar = st.session_state.get("sector_filtro_ransom", "Todos")
        controles_rec = st.session_state.get("controles_ransom", [])
        from ingestor.ransomware_feed import estadisticas_por_sector as es
        
        st.success(f"✅ {len(riesgos)} ataques encontrados")
        
        st.markdown("#### 📋 Víctimas recientes")
        df_data = []
        for r in riesgos:
            df_data.append({
                "Grupo": r["grupo"], "Víctima": r["victima"], "País": r["pais"],
                "Sector": r["sector"], "Fecha": r["fecha"],
                "Nivel Riesgo": r["nivel_riesgo"], "Score": f'{r["score"]}/25',
                "Descripción del Ataque": r.get("descripcion_ataque", r.get("descripcion", "No disponible")),
                "Justificación Controles": r.get("justificacion", "No disponible"),
            })
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True, column_config={
            "Descripción del Ataque": st.column_config.TextColumn(width="large"),
            "Justificación Controles": st.column_config.TextColumn(width="large"),
        })
        
        st.markdown("#### 📊 Afectación por sector")
        stats_sector = es(riesgos)
        if stats_sector:
            cols = st.columns(min(len(stats_sector), 4))
            for i, (sector, data) in enumerate(sorted(stats_sector.items(), key=lambda x: -x[1]["conteo"])):
                with cols[i % 4]:
                    color = "🔴" if data["nivel_promedio"] == "EXTREMO" else "🟠" if data["nivel_promedio"] == "ALTO" else "🟡"
                    st.metric(f"{color} {sector}", f'{data["conteo"]} ataques', data["nivel_promedio"])
        
        st.markdown("#### 🛡️ Controles ISO 27002 recomendados")
        if controles_rec:
            cols_iso = st.columns(len(controles_rec))
            for i, c in enumerate(controles_rec):
                with cols_iso[i]:
                    st.markdown(f"""
                    <div style="background:rgba(88,200,242,0.08);border:1px solid rgba(88,200,242,0.15);
                                border-radius:8px;padding:12px;text-align:center;">
                        <div style="color:#58C8F2;font-size:20px;font-weight:800;">{c['codigo']}</div>
                        <div style="color:rgba(255,255,255,0.6);font-size:11px;margin-top:4px;">{c['nombre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # ── Botón para generar y descargar Excel ──
        st.markdown("---")
        
        col_ex1, col_ex2 = st.columns([2, 1])
        with col_ex1:
            if st.button("📥 Generar Excel de Riesgos (con datos)", type="primary", key="btn_gen_excel"):
                from openpyxl import Workbook
                from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
                from datetime import datetime
                import tempfile, os
                
                wb = Workbook()
                ws = wb.active
                ws.title = "Riesgos Ransomware"
                
                hf = PatternFill(start_color="1B273D", end_color="1B273D", fill_type="solid")
                hfn = Font(color="FFFFFF", bold=True, size=11)
                bd = Border(left=Side(style='thin', color='CCCCCC'), right=Side(style='thin', color='CCCCCC'),
                            top=Side(style='thin', color='CCCCCC'), bottom=Side(style='thin', color='CCCCCC'))
                fe = PatternFill(start_color="FF4444", end_color="FF4444", fill_type="solid")
                fa = PatternFill(start_color="FF8800", end_color="FF8800", fill_type="solid")
                fm = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
                
                headers = ["Grupo", "Víctima", "País", "Sector", "Fecha", "Probabilidad", "Severidad", "Score", "Nivel Riesgo", "Descripción del Ataque", "Justificación de Controles ISO 27002"]
                for col, h in enumerate(headers, 1):
                    c = ws.cell(row=1, column=col, value=h)
                    c.fill = hf; c.font = hfn; c.alignment = Alignment(horizontal='center'); c.border = bd
                
                for row, r in enumerate(riesgos, 2):
                    dr = [r["grupo"], r["victima"], r["pais"], r["sector"], r["fecha"],
                          r["probabilidad"], r["severidad"], f'{r["score"]}/25', r["nivel_riesgo"],
                          r.get("descripcion_ataque", r.get("descripcion", "No disponible")),
                          r.get("justificacion", "No disponible")]
                    for col, val in enumerate(dr, 1):
                        c = ws.cell(row=row, column=col, value=val)
                        c.border = bd
                        if col == 9:
                            if val == "EXTREMO": c.fill = fe; c.font = Font(bold=True, color="FFFFFF")
                            elif val == "ALTO": c.fill = fa; c.font = Font(bold=True)
                            elif val == "MEDIO": c.fill = fm
                
                for col in range(1, len(headers)+1):
                    ws.column_dimensions[chr(64+col) if col <= 26 else 'Z'].width = 20
                
                ws2 = wb.create_sheet("Controles ISO 27002")
                for col, h in enumerate(["Código", "Nombre del Control", "Sector Recomendado"], 1):
                    c = ws2.cell(row=1, column=col, value=h)
                    c.fill = hf; c.font = hfn; c.border = bd
                for i, ctrl in enumerate(controles_rec, 2):
                    ws2.cell(row=i, column=1, value=ctrl["codigo"]).border = bd
                    ws2.cell(row=i, column=2, value=ctrl["nombre"]).border = bd
                    ws2.cell(row=i, column=3, value=sector_filtro_mostrar).border = bd
                
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
                wb.save(tmp.name)
                tmp.close()
                with open(tmp.name, 'rb') as f:
                    st.session_state["excel_datos"] = f.read()
                os.unlink(tmp.name)
                st.rerun()
        
        with col_ex2:
            if "excel_datos" in st.session_state:
                st.download_button(
                    "⬇️ Descargar Excel",
                    data=st.session_state["excel_datos"],
                    file_name=f"Threat_Intelligence_Ransomware_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_ransom_excel"
                )
            else:
                st.info("Pulsa 'Generar Excel'\ny luego descarga aquí")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Autodiagnóstico de Madurez ───────────────────────────────────────
