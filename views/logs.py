from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🔍 Registro de Eventos — Control A.8.15 ISO/IEC 27001:2022")
    st.markdown("Trazabilidad completa de accesos y análisis realizados en la plataforma.")

    col_r, col_d = st.columns([1, 1])
    with col_r:
        if st.button("🔄 Refrescar", key="btn_refresh_logs"):
            st.rerun()
    with col_d:
        entries = get_log_entries(200)
        if entries:
            import json as _json
            raw = "\n".join([_json.dumps(e, ensure_ascii=False) for e in entries])
            st.download_button("⬇️ Exportar Logs (.jsonl)", data=raw, file_name="audit_log.jsonl", mime="application/json")

    entries = get_log_entries(100)
    if not entries:
        st.info("No hay eventos registrados aún.")
    else:
        st.markdown(f"**{len(entries)} eventos registrados**")
        tabla_logs = "<table class='result-table'><tr><th>Timestamp (UTC)</th><th>Evento</th><th>Usuario</th><th>Resultado</th><th>Detalle</th></tr>"
        for e in reversed(entries):
            ts = e.get('timestamp','')[:19].replace('T',' ')
            evento = e.get('event', '')
            usr = e.get('user', '')
            res = e.get('result', '')
            det = e.get('detail', '')
            color = '#34d399' if res == 'success' else '#f87171'
            badge = f"<span style='color:{color};font-weight:600'>{res.upper()}</span>"
            tabla_logs += f"<tr><td style='font-size:0.8rem;color:#94a3b8'>{ts}</td><td><b>{evento}</b></td><td>{usr}</td><td>{badge}</td><td style='font-size:0.82rem'>{det}</td></tr>"
        tabla_logs += "</table>"
        st.markdown(tabla_logs, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

