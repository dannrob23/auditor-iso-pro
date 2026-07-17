from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🗂️ Historial de Reportes")
    
    todos_reportes = listar_reportes(200)
    if not todos_reportes:
        st.info("No hay reportes guardados aún.")
    else:
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        filtro_nombre = col_f1.text_input("🔍 Filtrar por nombre del documento", key="hist_filtro_nombre")
        min_pct, max_pct = col_f2.slider(
            "📈 Porcentaje de cumplimiento",
            0, 100, (0, 100),
            key="hist_filtro_pct"
        )
        
        reportes_filtrados = []
        for r in todos_reportes:
            nombre_doc = r.get("nombre_doc", "")
            pct = r.get("cumplimiento_pct", 0.0)
            if filtro_nombre and filtro_nombre.lower() not in nombre_doc.lower():
                continue
            if not (min_pct <= pct <= max_pct):
                continue
            reportes_filtrados.append(r)
            
        col_f3.markdown(f"<div style='text-align:right;padding-top:25px;font-size:0.9rem;color:rgba(255,255,255,0.6)'>Encontrados: <b>{len(reportes_filtrados)}</b> / {len(todos_reportes)}</div>", unsafe_allow_html=True)
        
        if not reportes_filtrados:
            st.warning("Ningún reporte coincide con los criterios de búsqueda.")
        else:
            items_por_pagina = 10
            total_paginas = ((len(reportes_filtrados) - 1) // items_por_pagina) + 1
            
            if "pagina_actual" not in st.session_state:
                st.session_state["pagina_actual"] = 1
                
            if st.session_state["pagina_actual"] > total_paginas:
                st.session_state["pagina_actual"] = total_paginas
            if st.session_state["pagina_actual"] < 1:
                st.session_state["pagina_actual"] = 1
                
            inicio = (st.session_state["pagina_actual"] - 1) * items_por_pagina
            fin = inicio + items_por_pagina
            
            for r in reportes_filtrados[inicio:fin]:
                ts = r["created_at"][:16].replace("T", " ")
                pct = r["cumplimiento_pct"]
                with st.expander(f"📄 {r['nombre_doc']} — {ts} — {pct}% cumplimiento"):
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("✅ Conformes",    r["conformes"])
                    col_b.metric("⚠️ Parciales",    r["parciales"])
                    col_c.metric("❌ No conformes", r["no_conformes"])
                    st.markdown(f"**Modelo:** {r['proveedor']} / {r['modelo']}  |  **Usuario:** {r['usuario']}")
                    st.markdown("---")
                    st.markdown(r["resultado"])
                    col_dl1, col_dl2, col_dl3 = st.columns(3)
                    with col_dl1:
                        st.download_button(
                            "⬇️ .md",
                            data=r["resultado"],
                            file_name=f"reporte_{r['id']}.md",
                            mime="text/markdown",
                            key=f"md_{r['id']}",
                        )
                    with col_dl2:
                        stats_r = {"conformes": r["conformes"], "parciales": r["parciales"],
                                   "no_conformes": r["no_conformes"], "cumplimiento_pct": r["cumplimiento_pct"]}
                        pdf_b = generar_pdf(r["resultado"], r["nombre_doc"], r["usuario"],
                                            r["proveedor"], r["modelo"], stats_r)
                        st.download_button(
                            "📄 Simple",
                            data=pdf_b,
                            file_name=f"reporte_{r['id']}.pdf",
                            mime="application/pdf",
                            key=f"pdf_{r['id']}",
                        )
                    with col_dl3:
                        from pdf_export import generar_informe_auditoria_profesional
                        prof_b = generar_informe_auditoria_profesional(
                            resultado_md=r["resultado"],
                            nombre_empresa=r["nombre_doc"],
                            sector="",
                            tamano_empresa="",
                            nombre_doc=r["nombre_doc"],
                            usuario=r["usuario"],
                            proveedor=r["proveedor"],
                            modelo=r["modelo"],
                            stats=stats_r,
                        )
                        st.download_button(
                            "📄 Profesional",
                            data=prof_b,
                            file_name=f"informe_{r['id']}.pdf",
                            mime="application/pdf",
                            key=f"prof_{r['id']}",
                        )
            
            if total_paginas > 1:
                st.markdown("---")
                col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
                with col_p1:
                    if st.button("⬅️ Anterior", disabled=(st.session_state["pagina_actual"] == 1), key="btn_pag_prev"):
                        st.session_state["pagina_actual"] -= 1
                        st.rerun()
                with col_p2:
                    st.markdown(f"<div class='pag-info'>Página <b>{st.session_state['pagina_actual']}</b> de {total_paginas}</div>", unsafe_allow_html=True)
                with col_p3:
                    if st.button("Siguiente ➡️", disabled=(st.session_state["pagina_actual"] == total_paginas), key="btn_pag_next"):
                        st.session_state["pagina_actual"] += 1
                        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 4: Logs de Auditoría ─────────────────────────────────────────────────
