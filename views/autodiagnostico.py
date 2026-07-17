from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    from autodiagnostico import mostrar_autodiagnostico
    mostrar_autodiagnostico()

    # Manejar generación con IA
    if st.session_state.get("generar_auto_propuesta", False):
        st.session_state["generar_auto_propuesta"] = False
        prompt = st.session_state.get("auto_prompt", "")
        if prompt:
            from langchain_core.messages import SystemMessage, HumanMessage
            with st.spinner("🤖 Generando propuesta personalizada..."):
                try:
                    llm_local_auto = None
                    if proveedor == "DeepSeek":
                        api_key_l = os.getenv("DEEPSEEK_API_KEY")
                        if api_key_l:
                            llm_local_auto = ChatOpenAI(model=modelo, temperature=temperatura, api_key=api_key_l, base_url="https://api.deepseek.com/v1")
                    elif proveedor == "Groq (Gratis)":
                        api_key_l = os.getenv("GROQ_API_KEY")
                        if api_key_l:
                            llm_local_auto = ChatOpenAI(model=modelo, temperature=temperatura, api_key=api_key_l, base_url="https://api.groq.com/openai/v1")
                    elif proveedor == "Google (Gemini)":
                        api_key_l = os.getenv("GOOGLE_API_KEY")
                        if api_key_l:
                            llm_local_auto = ChatGoogleGenerativeAI(model=modelo, temperature=temperatura, google_api_key=api_key_l)
                    else:
                        api_key_l = os.getenv("OPENAI_API_KEY")
                        if api_key_l:
                            llm_local_auto = ChatOpenAI(model=modelo, temperature=temperatura, api_key=api_key_l)

                    if llm_local_auto:
                        respuesta = llm_local_auto.invoke([
                            SystemMessage(content="Eres un consultor senior en ciberseguridad e IA para infraestructura crítica. Especialista en ISO 27001, ISO 42001, NIST AI RMF, ISO 19011 e ISO 23894."),
                            HumanMessage(content=prompt)
                        ])
                        st.session_state.auto_propuesta = respuesta.content
                    else:
                        st.error("No hay conexión con el proveedor de IA. Verifica la configuración.")
                except Exception as e:
                    st.error(f"Error generando propuesta: {e}")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Dashboard ─────────────────────────────────────────────────────────────
