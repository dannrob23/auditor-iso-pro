from views.common import *


from core import llm_factory
ejecutar_gap_analysis = llm_factory.ejecutar_gap_analysis


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### ✏️ Pega el texto de tu política directamente")
    texto_manual = st.text_area(
        "Texto de la política",
        placeholder="Pega aquí el contenido de tu política de seguridad de la información...",
        height=300,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if texto_manual.strip():
        if st.button("🔍 Ejecutar Gap Analysis", key="btn_texto"):
            log_event("GAP_ANALYSIS_START", user=usuario, detail=f"Texto libre | Modelo: {proveedor}/{modelo} | Chars: {len(texto_manual)}")
            with st.spinner("🤖 Analizando... por favor espera."):
                resultado = ejecutar_gap_analysis(texto_manual, proveedor, modelo, temperatura, usar_rag)
            stats = guardar_reporte(usuario, "Texto", "Análisis manual", proveedor, modelo, resultado)
            log_event("GAP_ANALYSIS_DONE", user=usuario, result="success", detail=f"Texto libre | Cumplimiento: {stats['cumplimiento_pct']}%")

            st.markdown("---")
            st.markdown("## 📊 Resultados del Gap Analysis")
            st.markdown(resultado)
            col_md2, col_pdf2, col_pro2 = st.columns(3)
            with col_md2:
                st.download_button("⬇️ (.md)", data=resultado,
                    file_name="gap_analysis_resultado.md", mime="text/markdown")
            with col_pdf2:
                pdf_bytes = generar_pdf(resultado, "Análisis manual", usuario, proveedor, modelo, stats)
                st.download_button("📄 PDF Simple", data=pdf_bytes,
                    file_name="gap_analysis_resultado.pdf", mime="application/pdf")
            with col_pro2:
                from pdf_export import generar_informe_auditoria_profesional
                aud_id = st.session_state.get("auditoria_actual_id")
                aud_data = obtener_auditoria(aud_id) if aud_id else None
                ctrls = st.session_state.get("controles_actuales", []) if st.session_state.get("controles_aid") == aud_id else None
                plan = st.session_state.get("plan_actual", {}) if st.session_state.get("controles_aid") == aud_id else None
                prof_bytes = generar_informe_auditoria_profesional(
                    resultado_md=resultado,
                    nombre_empresa=aud_data.get("nombre_empresa", "Análisis manual") if aud_data else "Análisis manual",
                    sector=aud_data.get("sector", "") if aud_data else "",
                    tamano_empresa=aud_data.get("tamano_empresa", "") if aud_data else "",
                    nombre_doc="Análisis manual",
                    usuario=usuario,
                    proveedor=proveedor,
                    modelo=modelo,
                    stats=stats,
                    controles_seleccionados=ctrls if ctrls and aud_id else None,
                    plan_implementacion=plan if plan and aud_id else None,
                )
                st.download_button("📄 PDF Profesional", data=prof_bytes,
                    file_name="informe_auditoria_manual.pdf", mime="application/pdf")

    # ── Tab Ruta de Auditoría ISO 27002 ──────────────────────────────────────────
