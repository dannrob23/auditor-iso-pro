from views.common import *
from services.analysis_service import analyze_pdf_policy
from core import llm_factory
from pdf_export import generar_informe_auditoria_profesional
extraer_texto_pdf = llm_factory.extraer_texto_pdf
ejecutar_gap_analysis = llm_factory.ejecutar_gap_analysis


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 📂 Sube tu política de seguridad (PDF)")
    archivo = st.file_uploader(
        "Arrastra o selecciona un archivo PDF",
        type=["pdf"],
        help="Sube el documento de política de seguridad que deseas auditar",
    )

    if archivo:
        with st.spinner("Extrayendo texto del PDF..."):
            texto = extraer_texto_pdf(archivo)
        palabras = len(texto.split())
        st.success(f"✅ Documento cargado — {palabras:,} palabras extraídas")

        col1, col2 = st.columns([3, 1])
        with col1:
            with st.expander("👁️ Vista previa del texto extraído"):
                st.text_area("", texto[:3000] + ("..." if len(texto) > 3000 else ""), height=200, disabled=True)
        with col2:
            st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='metric-value'>{palabras:,}</div><div class='metric-label'>Palabras analizadas</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔍 Ejecutar Gap Analysis", key="btn_pdf"):
            with st.spinner("🤖 El Auditor IA está analizando tu política... esto puede tardar 30-60 segundos."):
                resultado, stats, pdf_bytes, excel_bytes, _ = analyze_pdf_policy(
                    archivo, proveedor, modelo, temperatura, usar_rag, usuario
                )

            if resultado is None:
                st.error("El análisis falló. Intenta de nuevo.")
                return

            st.markdown("---")
            st.markdown("## 📊 Resultados del Gap Analysis")
            st.markdown(resultado)
            col_md, col_pdf, col_xls, col_pro = st.columns(4)
            with col_md:
                st.download_button("📄 .md", data=resultado,
                    file_name=f"gap_analysis_{archivo.name.replace('.pdf','')}.md", mime="text/markdown",
                    use_container_width=True)
            with col_pdf:
                st.download_button("📄 PDF", data=pdf_bytes,
                    file_name=f"gap_analysis_{archivo.name.replace('.pdf','')}.pdf", mime="application/pdf",
                    use_container_width=True)
            with col_xls:
                st.download_button("📊 Excel + Fuentes RAG", data=excel_bytes,
                    file_name=f"gap_analysis_{archivo.name.replace('.pdf','')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="xls_rag", type="primary", use_container_width=True)
            with col_pro:
                aud_id = st.session_state.get("auditoria_actual_id")
                aud_data = obtener_auditoria(aud_id) if aud_id else None
                ctrls = st.session_state.get("controles_actuales", []) if st.session_state.get("controles_aid") == aud_id else None
                plan = st.session_state.get("plan_actual", {}) if st.session_state.get("controles_aid") == aud_id else None
                if aud_data:
                    prof_bytes = generar_informe_auditoria_profesional(
                        resultado_md=resultado,
                        nombre_empresa=aud_data.get("nombre_empresa", archivo.name) if aud_data else archivo.name,
                        sector=aud_data.get("sector", "") if aud_data else "",
                        tamano_empresa=aud_data.get("tamano_empresa", "") if aud_data else "",
                        nombre_doc=archivo.name,
                        usuario=usuario,
                        proveedor=proveedor,
                        modelo=modelo,
                        stats=stats,
                        controles_seleccionados=ctrls if ctrls and aud_id else None,
                        plan_implementacion=plan if plan and aud_id else None,
                    )
                    st.download_button("📄 PDF Profesional", data=prof_bytes,
                        file_name=f"informe_auditoria_{archivo.name.replace('.pdf','')}.pdf", mime="application/pdf",
                        use_container_width=True)
                else:
                    st.info("Crea una auditoría\npara PDF profesional")
    else:
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Texto libre ───────────────────────────────────────────────────────
