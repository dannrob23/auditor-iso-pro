from views.common import *


from core import llm_factory
ejecutar_chat = llm_factory.ejecutar_chat


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 💬 Chat Interactivo con el Auditor")
    st.info(f"Modelo actual: **{proveedor} / {modelo}**")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿Qué deseas consultar sobre la normativa?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                full_response = ejecutar_chat(st.session_state.messages, proveedor, modelo, temperatura)
                st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 1: Subir PDF ─────────────────────────────────────────────────────────
