from views.common import *

# ── Paleta de colores de riesgo ──
RIESGO_COLORS = {
    "EXTREMO": {"bg": "rgba(239,68,68,0.18)",  "text": "#f87171", "border": "rgba(239,68,68,0.45)",  "hex": "#f87171"},
    "ALTO":    {"bg": "rgba(234,88,12,0.18)",  "text": "#fb923c", "border": "rgba(234,88,12,0.45)",  "hex": "#fb923c"},
    "MEDIO":   {"bg": "rgba(234,179,8,0.18)",  "text": "#fbbf24", "border": "rgba(234,179,8,0.45)",  "hex": "#fbbf24"},
    "BAJO":    {"bg": "rgba(52,211,153,0.18)", "text": "#34d399", "border": "rgba(52,211,153,0.45)", "hex": "#34d399"},
}

init_db()
load_dotenv()

from core.logo import get_logo_html, get_logo_base64

def _obtener_kb_dir():
    return Path("knowledge_base")

def _auto_descargar_fuentes():
    """Descarga fuentes en background con timeout para no bloquear el startup."""
    try:
        import threading
        def _descargar():
            kb = _obtener_kb_dir()
            # Si ya hay PDFs, indexar en background y salir
            if kb.exists() and any(kb.glob("*.pdf")):
                try:
                    indexar_documentos()
                except Exception:
                    pass
                return
            # Intentar descarga rápida (timeout corto para no bloquear)
            url = "https://github.com/dannrob23/auditor-iso-pro/releases/download/knowledge/knowledge_base_pdfs.zip"
            try:
                import requests, zipfile, io
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    kb.mkdir(exist_ok=True)
                    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                        for member in z.namelist():
                            if member.endswith(".pdf"):
                                target = kb / member.split("/")[-1]
                                target.write_bytes(z.read(member))
                    indexar_documentos()
            except Exception:
                pass
        hilo = threading.Thread(target=_descargar, daemon=True)
        hilo.start()
    except Exception:
        pass

_auto_descargar_fuentes()

# ── Configuración de página ──────────────────────────────────────────────────
_icon_img = "assets/logo.png" if Path("assets/logo.png").exists() else "🛡️"
st.set_page_config(
    page_title="AuditAI Pro | Auditoría de Ciberseguridad e IA",
    page_icon=_icon_img,
    layout="wide",
    initial_sidebar_state="expanded",
)

from core.theme import apply_theme
apply_theme()

# ── Autenticación ────────────────────────────────────────────────────────────
with open("config.yaml", encoding="utf-8") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.login()

if st.session_state.get("authentication_status") is False:
    log_event("LOGIN_FAILED", user=st.session_state.get("username", "unknown"), result="failure", detail="Credenciales incorrectas")
    st.error("⛔ Credenciales incorrectas. Acceso denegado.")
    st.stop()

if st.session_state.get("authentication_status") is None:
    logo_login_html = get_logo_html(size_px=80, extra_class="login-logo-hero")
    st.markdown(f"""
    <div class='cid-login-container'>
        <div class='cid-login-logo'>{logo_login_html}</div>
        <h1 class='cid-login-title'>AuditAI Pro</h1>
        <p class='cid-login-subtitle'>Plataforma de Auditoría de Ciberseguridad e Inteligencia Artificial</p>
        <div class='cid-login-frameworks'>
            ISO 27001 &middot; ISO 42001 &middot; NIST AI RMF &middot; ISO 19011 &middot; ISO 23894
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Usuario autenticado ──────────────────────────────────────────────────────
nombre = st.session_state.get("name", "Auditor")
usuario = st.session_state.get("username", "unknown")

# Registrar inicio de sesión exitoso (solo una vez por sesión)
if not st.session_state.get("_login_logged"):
    log_event("LOGIN_SUCCESS", user=usuario, result="success", detail=f"Sesión iniciada por {nombre}")
    st.session_state["_login_logged"] = True

from components.sidebar import render_sidebar
opcion_menu, proveedor, modelo, temperatura, usar_rag = render_sidebar(nombre, usuario, authenticator)
# ── Encabezado principal ─────────────────────────────────────────────────────
header_logo_html = get_logo_html(size_px=48, extra_class="header-logo-img")
st.markdown(f"""
<div class='cid-header'>
    <div class='cid-logo-wrapper'>{header_logo_html}</div>
    <div>
        <h1 class='cid-title'>AuditAI Pro</h1>
        <p class='cid-subtitle'>Plataforma Enterprise &middot; ISO 27001 &middot; ISO 42001 &middot; NIST AI RMF &middot; ISO 19011 &middot; ISO 23894</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Breadcrumb dinámico ─────────────────────────────────────────────────────
st.markdown(f"""
<div class='breadcrumb'>
  <span class='breadcrumb-item'>AuditAI Pro</span>
  <span class='breadcrumb-sep'>/</span>
  <span class='breadcrumb-item active'>{opcion_menu}</span>
</div>
""", unsafe_allow_html=True)

# ── Health Bar del sistema ────────────────────────────────────────────────────
_sv = stats_vulnerabilidades()
_total_vulns = int(_sv.get("total") or 0)
_sg = stats_globales()
_total_analisis = int(_sg.get("total_reportes") or 0)
try:
    _rag_ok = base_conocimiento_activa()
except Exception:
    _rag_ok = False
_rag_dot = "dot-green" if _rag_ok else "dot-yellow"
_rag_label = "RAG Activo" if _rag_ok else "RAG Inactivo"
_vuln_dot = "dot-green" if _total_vulns > 0 else "dot-yellow"
st.markdown(f"""
<div class='health-bar'>
  <span style='font-size:0.78rem;color:rgba(255,255,255,0.4);font-weight:600;letter-spacing:0.05em'>SISTEMA</span>
  <span class='health-item'><span class='health-dot {_rag_dot}'></span>{_rag_label}</span>
  <span class='health-item'><span class='health-dot {_vuln_dot}'></span>{_total_vulns} vulnerabilidades IA</span>
  <span class='health-item'><span class='health-dot dot-green'></span>{_total_analisis} análisis realizados</span>
  <span class='health-item'><span class='health-dot dot-green'></span>Modelo: {proveedor}</span>
</div>
""", unsafe_allow_html=True)

# ── Onboarding (primer uso) ───────────────────────────────────────────────────
if not st.session_state.get("_onboarding_done") and _total_analisis == 0:
    st.markdown("""
    <div class='onboarding-card'>
      <h3>👋 Bienvenido al IA-SEC Auditor Tool</h3>
      <p style='color:rgba(255,255,255,0.65);font-size:0.88rem;margin-bottom:12px'>Sigue estos pasos para realizar tu primer análisis:</p>
      <div class='onboarding-step'><span class='step-num'>1</span> Configura el proveedor de IA en el panel lateral</div>
      <div class='onboarding-step'><span class='step-num'>2</span> Ve a <b>📄 Auditoría de IA</b> y sube un PDF de política de seguridad</div>
      <div class='onboarding-step'><span class='step-num'>3</span> Haz clic en <b>🔍 Ejecutar Gap Analysis</b> y espera el resultado</div>
      <div class='onboarding-step'><span class='step-num'>4</span> Descarga el reporte en PDF o Markdown</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✅ Entendido, no mostrar de nuevo", key="btn_onboarding_ok"):
        st.session_state["_onboarding_done"] = True
        st.rerun()

# ── Tabs principales ─────────────────────────────────────────────────────────
# Eliminamos st.tabs y usamos opcion_menu del sidebar

# ── Tab 0: Chat Auditor ──────────────────────────────────────────────────────
if opcion_menu == "Chat Auditor":
    from views.chat_auditor import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Auditoría de IA":
    from views.auditora_de_ia import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Texto Libre":
    from views.texto_libre import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Ruta ISO 27002":
    from views.ruta_iso_27002 import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Base RAG":
    from views.base_rag import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Confluencia":
    from views.confluencia import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Interoperabilidad":
    from views.interoperabilidad import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Guía":
    from views.guia import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Rol Auditor":
    from views.rol_auditor import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Matriz Riesgos IA":
    from views.matriz_riesgos_ia import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "🔴 Threat Intelligence":
    from views._threat_intelligence import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "🔬 Autodiagnóstico":
    from views.autodiagnostico import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Dashboard":
    from views.dashboard import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Historial":
    from views.historial import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
if opcion_menu == "Logs":
    from views.logs import render
    render(usuario, nombre, proveedor, modelo, temperatura, usar_rag, opcion_menu)
# ── Footer CID INFOSEC (visible en todas las pantallas) ────────────────────
st.markdown(f"""
<div class='cid-footer'>
  <strong>AuditAI Pro</strong> v2.0 — Plataforma de Auditoría de Ciberseguridad e Inteligencia Artificial<br>
  &copy; {datetime.now().year} &middot; AuditAI Pro Inc. &middot; ISO 27001 &middot; ISO 42001 &middot; NIST AI RMF &middot; ISO 19011 &middot; ISO 23894<br>
  <span style='font-size:0.68rem;'>Confidencial &middot; Uso interno autorizado</span>
</div>
""", unsafe_allow_html=True)
