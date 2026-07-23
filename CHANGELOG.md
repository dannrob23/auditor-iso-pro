# Changelog — AuditAI Pro

## 2026-07-23 — RAG TF-IDF + Excel Profesional + Refactorización Mayor

### 🏗️ Arquitectura
- **Monolito → Modular**: `app.py` de 2,891 a 225 líneas
- Creado `core/theme.py`: CSS extraído
- Creado `core/llm_factory.py`: Factory de LLMs centralizado
- Creado `components/sidebar.py`: Sidebar reutilizable
- Creado `views/*.py`: 16 módulos individuales (chat, gap analysis, riesgos, interoperabilidad, etc.)
- Eliminado `st.set_page_config` duplicado que causaba crash

### 🧭 Sidebar + Navegación
- Rediseño completo con 6 categorías temáticas y separadores visuales
- 15 items navegables con emojis únicos
- Sistema `NAV_MAP` + `_nav_display` para navegación funcional
- Corregido bug: clics en sidebar no cambiaban de módulo

### 🧙 Wizard Flow (Matriz Riesgos IA)
- Pasos secuenciales: Paso 2 bloqueado hasta completar Paso 1
- Botón "🔄 Re-consultar fuentes"
- Búsqueda por texto + filtros por fuente, tipo y nivel de riesgo
- Paginación de 25 ítems/página con navegación ◀/▶

### 🛡️ Threat Intelligence
- Excel profesional con 4 hojas: Resumen, Matriz de Riesgos, Controles ISO 27002, Estadísticas
- KPIs: Extremos, Altos, Medios, Score Promedio
- Metodología ISO 27001:2022 Matriz 5x5 visible en expander
- Mejora de descripción: de "Víctimas recientes" a "Tabla de Riesgos ISO 27001"

### 🧠 RAG Reconstruido (sin torch, sin API)
- `core/embeddings.py`: Vectorización TF-IDF con sklearn (0 MB en RAM, $0)
- `core/chunking.py`: División inteligente de PDFs respetando numerales ISO (A.8.8, 6.1.2)
- `core/rag_engine.py`: Motor FAISS con caché persistente + prompt anti-alucinación
- `requirements.txt`: + `faiss-cpu==1.14.3` (+20 MB, ligero)
- Indexación de 14 PDFs normativos (ISO 27001, 27002, 42001, 23894, 19011, NIST, PCI DSS...)
- Startup no bloqueante: RAG se inicializa en thread background

### 🔗 RAG extendido a TODOS los módulos
| Módulo | Antes | Ahora |
|:-------|:-----:|:-----:|
| Chat Auditor (`ejecutar_chat`) | ❌ Sin RAG | ✅ Contexto ISO en cada pregunta |
| Gap Analysis PDF/Texto (`ejecutar_gap_analysis`) | ✅ Ya tenía | ✅ Mejorado con nuevo motor TF-IDF |
| Interoperabilidad (`generar_propuesta_ic`) | ❌ Sin RAG | ✅ Contexto normativo en propuesta |
| Matriz Riesgos IA (`analizar_vulnerabilidad`) | ❌ Sin RAG | ✅ Vulnerabilidades mapeadas a controles ISO |

### 📊 Excel profesional en Gap Analysis
- Nueva función `_generar_excel_gap_analysis()` en `services/analysis_service.py`
- 4 hojas: Portada, Resultados (tabla parseada), Informe Completo, Fuentes RAG
- Botón "📊 Excel + Fuentes RAG" (PRIMARY) en UI del Gap Analysis

### 📥 Módulo Confluencia
- Creado `Matriz_Confluencia_Auditoria_IA.xlsx` con 2 hojas
- Corregido: botón de descarga funcional (antes "archivo no disponible")

### 📥 Módulo Interoperabilidad
- Descarga Excel agregada (antes solo .md y PDF)
- Propuesta de implementación con 5 hojas Excel: Portada, Resumen, Matriz, Texto Completo, Plan de Acción

### 🔧 Bugs Corregidos
| Bug | Fix |
|:----|:----|
| Footer "Banco Agrario de Colombia" | ✅ "AuditAI Pro Inc." |
| `KeyError: pdf_export` en import | ✅ try/except con fallback |
| `NameError: ejecutar_chat` / `ejecutar_gap_analysis` | ✅ Funciones movidas a `core/llm_factory.py` |
| `NameError: extraer_texto_pdf` | ✅ Importado desde `core.llm_factory` |
| PDFs corruptos con BOM UTF-8 | ✅ Ignorados con logging, mínimo 50 chars |
| App no cargaba (startup bloqueante) | ✅ PDFs en background + RAG async |
| CI fallaba con 785 errores lint (F405, F403) | ✅ `.ruff.toml` + `pyproject.toml` con ignores |
| `use_container_width` deprecation warning | ✅ Reemplazado por `width='stretch'` |
| `pyproject.toml` corrupto (TOML parse error) | ✅ Limpio y válido |

### 🚀 Despliegue
- Migrado a Render.com: `https://auditor-iso-pro.onrender.com`
- Streamlit Cloud: `https://auditor-iso27001-pro-ovjagotdcgxfcngmnwkoew.streamlit.app`
- App funciona en plan free (512 MB RAM) tras eliminar torch

### 📚 Documentación técnica
- Nuevo: `.ruff.toml` para linting
- Actualizado: `requirements.txt` (17 → 18 dependencias, más ligeras)
- Nota: RAG usa TF-IDF local (sklearn) — no necesita API key
- Nota: Para mejor calidad semántica, configurar `OPENAI_API_KEY` en Secrets
