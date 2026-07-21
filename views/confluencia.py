from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🔗 Confluencia Normativa IA-SEC")
    st.markdown("**ISO 27001 + NIST AI RMF + ISO 42001 + ISO 19011 + ISO 23894** — 5 marcos integrados")
    st.markdown("""
    Esta sección muestra cómo se integran los marcos fundamentales para la auditoría de IA en infraestructura crítica.
    
    | Dimensión | ISO/IEC 27001:2022 | NIST AI RMF 1.0 | ISO/IEC 42001:2023 | ISO 19011:2018 | ISO 23894:2023 |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | **Gobernanza** | Cláusula 5: Liderazgo | Función GOVERN | Cláusula 5: Liderazgo AIMS | 6.2: Iniciación | 4: Principios |
    | **Riesgos** | 6.1.2: Evaluación | MAP/MEASURE | 6.1.2: Riesgos IA | 6.3: Preparación | 6.1: Proceso completo |
    | **Operación** | Anexo A: Controles | MANAGE | Anexo A: Controles IA | 6.4: Ejecución | 6.1.5: Tratamiento |
    | **Monitoreo** | A.8.16: Seguimiento | MEASURE | Cláusula 9: Evaluación | 6.5: Informe | 6.2: Monitoreo |
    | **Auditoría** | 9.2: Auditoría interna | — | 9.2: Auditoría interna | 6: Todo el ciclo | — |
    | **Privacidad** | A.8.10: Datos | Trustworthy AI | Anexo B: Impacto social | — | 6.2: Privacidad |
    | **Técnico** | A.8.8: Vulnerabilidades | Robustness & Safety | A.7: Desarrollo seguro | 6.4: Evidencia | 5.5: Adversarial |
    """)
    
    st.markdown("---")
    st.markdown("#### 📥 Entregable Académico")
    st.info("Descarga la matriz detallada de confluencia que articula los 5 marcos normativos para tu propuesta de auditoría de IA en infraestructura crítica.")
    try:
        with open("Matriz_Confluencia_Auditoria_IA.xlsx", "rb") as f:
            st.download_button(
                "⬇️ Descargar Matriz de Confluencia (Excel)",
                data=f,
                file_name="Matriz_Confluencia_Auditoria_IA.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn_matriz_conf"
            )
    except FileNotFoundError:
        st.warning("Archivo Matriz_Confluencia_Auditoria_IA.xlsx no disponible.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Interoperabilidad ─────────────────────────────────────────────────────
