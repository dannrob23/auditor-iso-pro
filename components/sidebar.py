import streamlit as st
from pathlib import Path
from rag_knowledge import base_conocimiento_activa

def render_sidebar(nombre, usuario, authenticator):
    # ── Sidebar ──────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:0.4rem;'>
            <div style='width:28px;height:28px;background:linear-gradient(135deg,#5e6ad2,#7170ff);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:0.9rem;flex-shrink:0;'>🛡️</div>
            <span style='font-size:0.95rem;font-weight:600;color:#f7f8f8;letter-spacing:-0.3px;'>AuditAI Pro</span>
        </div>
        <p style='font-size:0.76rem;color:#8a8f98;margin:0 0 0.8rem 0;'>Auditoría de Ciberseguridad e IA</p>
        """, unsafe_allow_html=True)
    
        st.markdown(f"**{nombre}**")
        st.markdown(f"<span style='font-size:0.76rem;color:#62666d;'>{usuario}</span>", unsafe_allow_html=True)
        st.markdown("---")
    
        # ── Navegación única con separadores visuales ──
        ALL_ITEMS = [
            "🔍 Auditoría",
            "💬 Chat Auditor",
            "🤖 Auditoría de IA",
            "📝 Texto Libre",
            "📋 Cumplimiento",
            "🛣️ Ruta ISO 27002",
            "📚 Base RAG",
            "🔗 Confluencia",
            "🔄 Interoperabilidad",
            "🛡️ Riesgos",
            "🗂️ Matriz Riesgos IA",
            "🚨 Threat Intelligence",
            "📊 Analítica",
            "📈 Dashboard",
            "📜 Historial",
            "📖 Recursos",
            "📖 Guía",
            "🎓 Rol Auditor",
            "📋 Logs",
            "🧪 Diagnóstico",
            "🩺 Autodiagnóstico",
        ]
        # Items que son separadores (no seleccionables)
        SEPARADORES = {"🔍 Auditoría", "📋 Cumplimiento", "🛡️ Riesgos", "📊 Analítica", "📖 Recursos", "🧪 Diagnóstico"}
    
        # Encontrar índice del último item seleccionado
        last = st.session_state.get("_nav_display", "💬 Chat Auditor")
        idx_map = {item: i for i, item in enumerate(ALL_ITEMS) if item not in SEPARADORES}
        default_idx = idx_map.get(last, 0)
    
        opcion_menu_raw = st.radio(
            "Navegación", ALL_ITEMS,
            index=default_idx,
            key="nav_unico",
            label_visibility="collapsed",
        )
    
        # Si es separador, revertir al anterior
        if opcion_menu_raw in SEPARADORES:
            opcion_menu_raw = st.session_state.get("_nav_display", "💬 Chat Auditor")
    
        # Mapeo a nombre original
        NAV_MAP = {
            "💬 Chat Auditor": "Chat Auditor",
            "🤖 Auditoría de IA": "Auditoría de IA",
            "📝 Texto Libre": "Texto Libre",
            "🛣️ Ruta ISO 27002": "Ruta ISO 27002",
            "📚 Base RAG": "Base RAG",
            "🔗 Confluencia": "Confluencia",
            "🔄 Interoperabilidad": "Interoperabilidad",
            "🗂️ Matriz Riesgos IA": "Matriz Riesgos IA",
            "🚨 Threat Intelligence": "🔴 Threat Intelligence",
            "📈 Dashboard": "Dashboard",
            "📜 Historial": "Historial",
            "📖 Guía": "Guía",
            "🎓 Rol Auditor": "Rol Auditor",
            "📋 Logs": "Logs",
            "🩺 Autodiagnóstico": "🔬 Autodiagnóstico",
        }
    
        opcion_menu = NAV_MAP.get(opcion_menu_raw, opcion_menu_raw)
        st.session_state["_nav_display"] = opcion_menu_raw
        st.session_state["_last_menu"] = opcion_menu
    
        st.markdown("---")
        st.markdown("<p style='font-size:0.74rem;color:#62666d;letter-spacing:0.05em;text-transform:uppercase;font-weight:500;margin-bottom:0.5rem;'>Entregables</p>", unsafe_allow_html=True)
        try:
            ruta_confluencia = Path("Matriz_Confluencia_Auditoria_IA.xlsx")
            if ruta_confluencia.exists():
                with open(ruta_confluencia, "rb") as f:
                    st.download_button(
                        "📊 Base: Matriz de Confluencia",
                        data=f,
                        file_name="Matriz_Confluencia_Auditoria_IA.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        except Exception as e:
            st.caption(f"⚠️ No disponible: {e}")
    
        # ── Botón de descarga del Excel de respaldo ──
        try:
            excel_respaldo = Path("data") / "Matriz_Riesgos_IA.xlsx"
            if excel_respaldo.exists():
                with open(excel_respaldo, "rb") as f:
                    st.download_button(
                        "🛡️ Matriz de Riesgos IA (Excel)",
                        data=f,
                        file_name="Matriz_Riesgos_IA.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="sidebar_excel_riesgos",
                    )
        except Exception as e:
            st.caption(f"⚠️ No disponible: {e}")
        st.markdown("---")
        with st.expander("⚙️ Config. Asistente IA", expanded=False):
            proveedor = st.selectbox(
                "Proveedor de IA",
                ["DeepSeek", "Groq (Gratis)", "OpenAI", "Google (Gemini)"],
                index=0,
            )
    
            if proveedor == "Google (Gemini)":
                modelo = st.selectbox("Modelo", ["gemini-1.5-pro", "gemini-1.5-flash"], index=0)
            elif proveedor == "DeepSeek":
                modelo = st.selectbox("Modelo", ["deepseek-chat", "deepseek-coder"], index=0)
            elif proveedor == "Groq (Gratis)":
                modelo = st.selectbox("Modelo", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"], index=0)
            else:
                modelo = st.selectbox("Modelo", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)
    
            temperatura = st.slider("Temperatura", 0.0, 1.0, 0.1, 0.05)
    
            usar_rag = st.checkbox("📚 Usar Base de Conocimiento RAG", value=True,
                                  help="Desactiva si experimentas problemas con la base de conocimiento")
    
            try:
                rag_activo = base_conocimiento_activa()
                st.caption("🟢 Base RAG operativa" if rag_activo else "🟡 Base RAG inactiva")
            except Exception:
                st.caption("🔴 Error en Base RAG")
    
        st.markdown("---")
        if st.session_state.get("authentication_status"):
            authenticator.logout("🚪 Cerrar sesión", location="sidebar")
    

    return opcion_menu, proveedor, modelo, temperatura, usar_rag
