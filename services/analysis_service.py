from core.llm_factory import ejecutar_gap_analysis, ejecutar_chat, extraer_texto_pdf
from database import guardar_reporte, guardar_vulnerabilidad
from audit_logger import log_event
from pdf_export import generar_pdf


def analyze_pdf_policy(archivo, proveedor, modelo, temperatura, usar_rag, usuario):
    texto = extraer_texto_pdf(archivo)
    palabras = len(texto.split())
    if palabras == 0:
        return None, 0, "No se pudo extraer texto del PDF."

    log_event("GAP_ANALYSIS_START", user=usuario, detail=f"Archivo: {archivo.name} | Modelo: {proveedor}/{modelo}")

    resultado = ejecutar_gap_analysis(texto, proveedor, modelo, temperatura, usar_rag)
    stats = guardar_reporte(usuario, "PDF", archivo.name, proveedor, modelo, resultado)

    log_event("GAP_ANALYSIS_DONE", user=usuario, result="success",
              detail=f"Archivo: {archivo.name} | Cumplimiento: {stats['cumplimiento_pct']}%")

    pdf_bytes = generar_pdf(resultado, archivo.name, usuario, proveedor, modelo, stats)
    return resultado, stats, pdf_bytes, texto


def analyze_text_policy(texto, proveedor, modelo, temperatura, usar_rag, usuario, nombre_doc="texto_manual"):
    palabras = len(texto.split())
    if palabras == 0:
        return None, 0, "El texto está vacío."

    log_event("GAP_ANALYSIS_START", user=usuario, detail=f"Texto libre | {palabras} palabras | Modelo: {proveedor}/{modelo}")

    resultado = ejecutar_gap_analysis(texto, proveedor, modelo, temperatura, usar_rag)
    stats = guardar_reporte(usuario, "TEXTO", nombre_doc, proveedor, modelo, resultado)

    log_event("GAP_ANALYSIS_DONE", user=usuario, result="success",
              detail=f"Texto libre | Cumplimiento: {stats['cumplimiento_pct']}%")

    pdf_bytes = generar_pdf(resultado, nombre_doc, usuario, proveedor, modelo, stats)
    return resultado, stats, pdf_bytes


def chat_with_auditor(mensajes, proveedor, modelo, temperatura):
    return ejecutar_chat(mensajes, proveedor, modelo, temperatura)
