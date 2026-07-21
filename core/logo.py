import base64
from pathlib import Path
import streamlit as st

@st.cache_data
def get_logo_base64() -> str:
    """Retorna el string Base64 del logo oficial de la aplicación."""
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        encoded = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""

def get_logo_html(size_px: int = 40, extra_class: str = "") -> str:
    """Genera el tag HTML <img> para incrustar el logo de forma fluida."""
    b64 = get_logo_base64()
    if b64:
        return f'<img src="{b64}" class="app-logo-img {extra_class}" style="height: {size_px}px; width: auto; object-fit: contain; vertical-align: middle; filter: drop-shadow(0 2px 8px rgba(94, 106, 210, 0.4));" alt="AuditAI Pro Logo" />'
    return '<span style="font-size: 1.5rem;">🛡️</span>'
