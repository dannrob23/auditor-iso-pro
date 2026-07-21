import streamlit as st
from pathlib import Path
from rag_knowledge import base_conocimiento_activa
from core.logo import get_logo_html

MENU_GROUPS = [
    ("🔍 AUDITORÍA & ANÁLISIS", [
        ("📄 Auditoría de IA", "Auditoría de IA"),
        ("💬 Chat Auditor", "Chat Auditor"),
        ("📝 Texto Libre", "Texto Libre"),
        ("🛣️ Ruta ISO 27002", "Ruta ISO 27002"),
    ]),
    ("📚 BASE DE CONOCIMIENTO & RAG", [
        ("📚 Base RAG", "Base RAG"),
        ("🔗 Confluencia", "Confluencia"),
        ("🔄 Interoperabilidad", "Interoperabilidad"),
    ]),
    ("📊 GESTIÓN & ANALÍTICA", [
        ("📈 Dashboard", "Dashboard"),
        ("🛡️ Matriz Riesgos IA", "Matriz Riesgos IA"),
        ("📜 Historial", "Historial"),
        ("📖 Guía", "Guía"),
        ("🎓 Rol Auditor", "Rol Auditor"),
    ]),
    ("⚙️ SISTEMA & SALUD", [
        ("🚨 Threat Intelligence", "🔴 Threat Intelligence"),
        ("🧪 Autodiagnóstico", "🔬 Autodiagnóstico"),
        ("📋 Logs", "Logs"),
    ]),
]

def render_sidebar(nombre, usuario, authenticator):
    with st.sidebar:
        logo_img = get_logo_html(size_px=42, extra_class="sidebar-logo-shadow")
        st.markdown(f"""
        <div class='sidebar-brand'>
            <div class='sidebar-brand-icon-wrapper'>{logo_img}</div>
            <div>
                <div class='sidebar-brand-title'>AuditAI Pro</div>
                <div class='sidebar-brand-sub'>Plataforma de Auditoría & IA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='user-profile-badge'>
            <div class='user-avatar'>👤</div>
            <div class='user-info'>
                <div class='user-name'>{nombre}</div>
                <div class='user-role'>{usuario} &middot; <span style="color:#10b981;">Auditor Activo</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='nav-sidebar-separator'></div>", unsafe_allow_html=True)

        current_route = st.session_state.get("_last_menu", "Chat Auditor")

        for group_idx, (group_name, items) in enumerate(MENU_GROUPS):
            st.markdown(f"<div class='nav-section-header'>{group_name}</div>", unsafe_allow_html=True)

            for display, route in items:
                is_active = (route == current_route)
                key = f"nav_btn_{route}"

                if st.button(
                    display,
                    key=key,
                    type="primary" if is_active else "secondary",
                    use_container_width=True,
                ):
                    st.session_state["_last_menu"] = route
                    st.session_state["_nav_display"] = display
                    st.rerun()

            if group_idx < len(MENU_GROUPS) - 1:
                st.markdown("<div class='nav-group-divider'></div>", unsafe_allow_html=True)

        st.markdown("<div class='nav-sidebar-separator'></div>", unsafe_allow_html=True)

        st.markdown("<p style='font-size:0.74rem;color:#8a8f98;letter-spacing:0.05em;text-transform:uppercase;font-weight:600;margin-bottom:0.5rem;'>📦 ENTREGABLES AUDITORÍA</p>", unsafe_allow_html=True)
        try:
            ruta_confluencia = Path("Matriz_Confluencia_Auditoria_IA.xlsx")
            if ruta_confluencia.exists():
                with open(ruta_confluencia, "rb") as f:
                    st.download_button(
                        "📊 Base: Matriz de Confluencia",
                        data=f,
                        file_name="Matriz_Confluencia_Auditoria_IA.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
        except Exception as e:
            st.caption(f"⚠️ No disponible: {e}")

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
                        use_container_width=True,
                    )
        except Exception as e:
            st.caption(f"⚠️ No disponible: {e}")

        st.markdown("<div class='nav-sidebar-separator'></div>", unsafe_allow_html=True)

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

        st.markdown("<div class='nav-sidebar-separator'></div>", unsafe_allow_html=True)
        if st.session_state.get("authentication_status"):
            authenticator.logout("🚪 Cerrar sesión", location="sidebar")

    opcion_menu = st.session_state.get("_last_menu", "Chat Auditor")
    return opcion_menu, proveedor, modelo, temperatura, usar_rag
