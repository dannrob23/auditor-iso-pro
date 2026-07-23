from views.common import *


def render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu):
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 📚 Base de Conocimiento Oficial (Modo NotebookLM)")
    st.markdown("Sube los PDFs oficiales de la norma ISO/IEC 27001 a la carpeta `knowledge_base/` para que la IA ancle sus respuestas a la realidad.")
    
    estado_rag = "✅ Activa" if base_conocimiento_activa() else "❌ Inactiva / Vacía"
    st.markdown(f"**Estado actual de la base RAG:** {estado_rag}")

    # Información adicional sobre el estado
    try:
        from pathlib import Path
        data_dir = Path("data")
        faiss_dir = data_dir / "faiss_index"
        knowledge_dir = Path("knowledge_base")

        num_docs = len(list(knowledge_dir.glob("*.pdf"))) + len(list(knowledge_dir.glob("*.txt"))) + len(list(knowledge_dir.glob("*.docx")))

        if faiss_dir.exists():
            faiss_size = (faiss_dir / "index.faiss").stat().st_size if (faiss_dir / "index.faiss").exists() else 0
            st.info(f"📊 {num_docs} documentos indexados | Índice: {faiss_size:,} bytes")
        else:
            st.warning("📊 Base de datos FAISS no encontrada")

    except Exception as e:
        st.error(f"Error verificando estado: {e}")
    
    col_idx1, col_idx2 = st.columns(2)
    with col_idx1:
        if st.button("🔄 Indexar documentos de la norma"):
            with st.spinner("Fragmentando y vectorizando documentos con modelo local (esto puede tardar la primera vez)..."):
                num_chunks, msg = indexar_documentos()
                if num_chunks > 0:
                    st.success(msg)
                    log_event("RAG_INDEX_UPDATE", user=usuario, result="success", detail=msg)
                else:
                    st.warning(msg)

    with col_idx2:
        if st.button("🔧 Diagnosticar/Reconstruir índice", help="Usa esto si experimentas errores con RAG"):
            with st.spinner("Diagnosticando y reconstruyendo índice..."):
                try:
                    # Importar aquí para evitar problemas si no está disponible
                    import subprocess
                    result = subprocess.run([sys.executable, "regenerar_indice.py"],
                                          capture_output=True, text=True, cwd=os.getcwd())
                    if result.returncode == 0:
                        st.success("Índice reconstruido exitosamente")
                        st.rerun()  # Recargar para actualizar estado
                    else:
                        st.error(f"Error reconstruyendo índice: {result.stderr}")
                except Exception as e:
                    st.error(f"Error ejecutando diagnóstico: {e}")
                

    # Uploader temporal aislado: no toca knowledge_base/
    st.markdown("---")
    st.markdown("#### 📤 Documentos temporales (carga puntual)")
    st.caption("Estos archivos solo se usan para la sesión actual y no alteran la base oficial de conocimiento.")
    archivos_subidos = st.file_uploader(
        "Arrastra PDFs, TXTs o DOCXs aquí",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        key="rag_uploader_temporal",
    )
    if archivos_subidos:
        from pathlib import Path as _Path
        UPLOADS_DIR = _Path("uploads")
        UPLOADS_DIR.mkdir(exist_ok=True)
        guardados = []
        for archivo in archivos_subidos:
            ruta_destino = UPLOADS_DIR / archivo.name
            with open(ruta_destino, "wb") as f:
                f.write(archivo.getbuffer())
            guardados.append(archivo.name)
        st.success(f"✅ {len(guardados)} archivos subidos: {', '.join(guardados)}")

    col_up1, col_up2, col_up3 = st.columns(3)
    with col_up1:
        if st.button("🔄 Indexar uploads", key="btn_indexar_uploads"):
            with st.spinner("Indexando documentos temporales..."):
                try:
                    num_chunks, msg = indexar_documentos_temporales()
                    if num_chunks > 0:
                        st.success(msg)
                    else:
                        st.warning(msg)
                except Exception as e:
                    st.error(f"No se pudo indexar uploads en este entorno: {e}")
    with col_up2:
        if st.button("🧹 Limpiar uploads", key="btn_limpiar_uploads"):
            try:
                limpiar_uploads()
                st.success("Uploads temporales eliminados.")
                st.rerun()
            except Exception as e:
                st.error(f"No se pudo limpiar uploads: {e}")
    with col_up3:
        try:
            if base_uploads_activa():
                st.markdown("**Uploads activos:** ✅")
            else:
                st.markdown("**Uploads activos:** —")
        except Exception:
            st.markdown("**Uploads activos:** —")
    st.info("💡 **Cómo funciona:** El sistema busca en el 'Marco de Gobernanza' (NIST/ISO42001) y en los estándares de ciberseguridad (ISO27001 e ISO 27002) para anclar la evaluación a requisitos reales de las normas.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab Confluencia ──────────────────────────────────────────────────────────
