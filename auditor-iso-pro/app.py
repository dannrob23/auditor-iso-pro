import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
import tempfile

# 1. Configuración de Seguridad
st.set_page_config(page_title="Audit-AI Pro", page_icon="🛡️")

def check_auth():
    if "auth" not in st.session_state:
        st.title("🛡️ Acceso Auditoría")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if u == st.secrets["USER_LOGIN"] and p == st.secrets["USER_PASS"]:
                st.session_state.auth = True
                st.rerun()
            else: st.error("Acceso Denegado")
        return False
    return True

if check_auth():
    st.title("🛡️ Sistema de Pre-Auditoría ISO 27001")
    st.sidebar.info("Modo: Auditoría de Brechas (Gap Analysis)")

    # 2. Carga de Documentación
    uploaded_file = st.file_uploader("Sube la Política de Seguridad (PDF)", type="pdf")

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        if st.button("🔥 Iniciar Auditoría Irruptiva"):
            with st.spinner("Analizando contra estándar ISO 27001:2022..."):
                try:
                    # Lógica RAG simplificada para MVP
                    loader = PyPDFLoader(tmp_path)
                    docs = loader.load()
                    content = "\n".join([d.page_content for d in docs[:5]]) # Analiza primeras 5 pág.

                    llm = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAI_API_KEY"])
                    
                    # Llamada al cerebro de auditoría
                    response = llm.invoke(f"Analiza esta política bajo ISO 27001:\n\n{content}")
                    
                    st.markdown("### 📊 Informe de Hallazgos")
                    st.write(response.content)
                    st.success("Auditoría completada. Prepárate para los ajustes.")
                except Exception as e:
                    st.error(f"Error técnico: {e}")
