from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    from guia_auditor import mostrar_rol_auditor
    mostrar_rol_auditor()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Matriz de Riesgos IA ──────────────────────────────────────────────
