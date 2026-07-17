from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    from guia_auditor import mostrar_guia_mejorada
    mostrar_guia_mejorada()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Rol del Auditor (ISO 19011 + ISO 23894 + Base de Conocimiento) ─────
