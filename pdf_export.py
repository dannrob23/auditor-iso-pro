"""
Módulo de exportación a PDF — Reportes de Gap Analysis ISO/IEC 27001:2022
Utiliza ReportLab para generar reportes profesionales.
"""
import io
import re
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, KeepTogether
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    _REPORTLAB_OK = True
except Exception:
    from typing import Any
    _REPORTLAB_OK = False
    class _mock:
        def __init__(self, *a, **kw): pass
        def hexval(self): return "000000"
        def __getattr__(self, n): return self
    colors = type('colors', (), {'HexColor': lambda *a: _mock(), 'white': _mock(), 'black': _mock()})()
    A4 = (595, 842)
    cm = 28.35
    TA_CENTER = 1
    TA_LEFT = 0
    def getSampleStyleSheet(): return type('ss', (), {'__getattr__': lambda s, k: type('s',(),{'__getitem__':lambda s,k: type('p')(), 'fontName':'','fontSize':9})()})()
    ParagraphStyle = lambda *a,**kw: type('p',(),{})()
    SimpleDocTemplate = lambda *a,**kw: type('d',(),{'build':lambda s,o: None})()
    Spacer = lambda *a,**kw: None
    Table = lambda *a,**kw: type('t',(),{'setStyle':lambda s,o: None})()
    HRFlowable = lambda *a,**kw: None
    KeepTogether = lambda *a,**kw: None
    Paragraph = lambda *a,**kw: type('p',(),{'__str__':lambda s:''})()

# ── Paleta de colores ────────────────────────────────────────────────────────
COLOR_PURPLE    = colors.HexColor("#7c3aed")
COLOR_BLUE      = colors.HexColor("#2563eb")
COLOR_GREEN     = colors.HexColor("#059669")
COLOR_YELLOW    = colors.HexColor("#d97706")
COLOR_RED       = colors.HexColor("#dc2626")
COLOR_DARK      = colors.HexColor("#1e1b4b")
COLOR_GRAY_BG   = colors.HexColor("#f8f7ff")
COLOR_GRAY_TEXT = colors.HexColor("#64748b")
COLOR_WHITE     = colors.white


def _parse_md_table(resultado: str) -> tuple[list[str], list[list[str]]]:
    """Extrae cabeceras y filas de la tabla Markdown del resultado."""
    lines = [l.strip() for l in resultado.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    headers = [c.strip() for c in lines[0].split("|") if c.strip()]
    rows = []
    for line in lines[2:]:  # saltar separador ---
        cells = [c.strip() for c in line.split("|") if c.strip() != ""]
        if cells:
            rows.append(cells)
    return headers, rows


def _estado_color(texto: str):
    t = texto.upper()
    if "CONFORME" in t and "NO" not in t:
        return COLOR_GREEN
    elif "PARCIAL" in t:
        return COLOR_YELLOW
    elif "NO CONFORME" in t or "❌" in t:
        return COLOR_RED
    return COLOR_GRAY_TEXT


def _pdf_sin_reportlab(mensaje: str) -> bytes:
    """Retorna un PDF mínimo de texto si reportlab no está instalado."""
    texto = f"PDF no disponible: falta reportlab. {mensaje}"
    return texto.encode("utf-8") if not _REPORTLAB_OK else b""


def generar_pdf_propuesta_interoperabilidad(
    propuesta: str,
    sector_id: str,
    sector_nombre: str,
    controles_evaluados: dict,
    usuario: str,
    proveedor: str,
    modelo: str,
) -> bytes:
    """Genera un PDF especializado para propuestas de interoperabilidad."""
    if not _REPORTLAB_OK:
        return _pdf_sin_reportlab("propuesta_interoperabilidad")
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"Propuesta Interoperabilidad IC - {sector_nombre}",
        author="Auditor ISO/IEC 27001:2022 IA",
    )

    styles = getSampleStyleSheet()
    story = []

    # ── Encabezado ────────────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=18, textColor=COLOR_PURPLE,
        spaceAfter=4, alignment=TA_CENTER,
    )
    sub_style = ParagraphStyle(
        "Sub", parent=styles["Normal"],
        fontSize=12, textColor=COLOR_GRAY_TEXT,
        alignment=TA_CENTER, spaceAfter=4,
    )
    story.append(Paragraph("AuditAI Pro — Propuesta de Implementación", title_style))
    story.append(Paragraph("ISO 27001 · ISO 42001 · NIST AI RMF · ISO 19011 · ISO 23894 para Infraestructuras Críticas", sub_style))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_PURPLE, spaceAfter=12))

    # ── Metadatos ─────────────────────────────────────────────────────────────
    meta_data = [
        ["Sector de Infraestructura Crítica:", sector_nombre],
        ["Identificador del sector:", sector_id.upper()],
        ["Auditor (usuario):", usuario],
        ["Modelo de IA:", f"{proveedor} / {modelo}"],
        ["Fecha de generación:", datetime.now().strftime("%d/%m/%Y %H:%M UTC")],
        ["Controles evaluados:", str(len(controles_evaluados))],
        ["Estándares evaluados:", "ISO/IEC 27001:2022 · ISO/IEC 42001:2023 · NIST AI RMF 1.0 · ISO 19011 · ISO 23894"],
        ["Metodología de auditoría:", "ISO 19011:2018 — 5 fases (Iniciación, Preparación, Ejecución, Informe, Seguimiento)"],
        ["Gestión de riesgos de IA:", "ISO/IEC 23894:2023 — 7 categorías de riesgo de IA"],
    ]
    meta_style = ParagraphStyle("meta", fontSize=9, leading=14)
    meta_table = Table(meta_data, colWidths=[6*cm, 10*cm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), COLOR_DARK),
        ("TEXTCOLOR", (1, 0), (1, -1), COLOR_GRAY_TEXT),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_GRAY_BG),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Resumen Ejecutivo ─────────────────────────────────────────────────────
    # Calcular estadísticas de evaluación con los nuevos estados
    total_eval = len(controles_evaluados) if controles_evaluados else 1
    c_total = sum(1 for v in controles_evaluados.values() if v == "Cumplimiento total")
    c_mayor = sum(1 for v in controles_evaluados.values() if v == "Mayormente implementado")
    c_parcial = sum(1 for v in controles_evaluados.values() if v == "Implementado parcialmente")
    c_inicial = sum(1 for v in controles_evaluados.values() if v == "En proceso inicial")
    c_no = sum(1 for v in controles_evaluados.values() if v == "No iniciado")

    section_style = ParagraphStyle(
        "Section", fontSize=12, textColor=COLOR_PURPLE,
        fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6,
    )
    story.append(Paragraph("Resumen Ejecutivo de Evaluación", section_style))

    resumen_data = [
        ["Estado de Implementación", "Cantidad", "Porcentaje"],
        ["[OK] Cumplimiento total", str(c_total), f"{c_total/total_eval*100:.1f}%"],
        ["[ALTO] Mayormente implementado", str(c_mayor), f"{c_mayor/total_eval*100:.1f}%"],
        ["[MEDIO] Implementado parcialmente", str(c_parcial), f"{c_parcial/total_eval*100:.1f}%"],
        ["[BAJO] En proceso inicial", str(c_inicial), f"{c_inicial/total_eval*100:.1f}%"],
        ["[CRITICO] No iniciado", str(c_no), f"{c_no/total_eval*100:.1f}%"],
    ]
    resumen_table = Table(resumen_data, colWidths=[9*cm, 3*cm, 4*cm])
    resumen_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), COLOR_PURPLE),
        ("TEXTCOLOR",     (0, 0), (-1, 0), COLOR_WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ALIGN",         (1, 0), (2, -1), "CENTER"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
    ]))
    story.append(resumen_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Contenido de la propuesta ─────────────────────────────────────────────
    story.append(Paragraph("Propuesta de Implementación Detallada", section_style))

    body_style = ParagraphStyle("body", fontSize=9, leading=12, spaceAfter=4)
    code_style = ParagraphStyle("code", fontSize=7, leading=9, spaceAfter=2,
                                 fontName="Courier", textColor=colors.HexColor("#555555"))
    in_code_block = False
    for line in propuesta.splitlines():
        # Detectar bloques de código (mermaid, diagramas ASCII)
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue  # Saltar diagramas ASCII/mermaid
        if not line.strip():
            story.append(Spacer(1, 0.2*cm))
            continue

        # Limpiar caracteres no imprimibles con Helvetica
        cleaned = line
        # Emoji y símbolos → texto plano
        replacements = {
            "🧩": "", "📋": "", "✅": "[OK]", "❌": "[X]", "🟢": "[OK]",
            "🟡": "[~]", "🟠": "[!]", "🔴": "[!]", "⚠️": "[!]",
            "■": ">", "▪": ">", "▫": ">", "►": ">", "○": "-",
            "●": "-", "◆": ">", "◇": ">", "☑": "[x]", "□": "[ ]",
            "↑": "^", "↓": "v", "→": "->", "←": "<-",
            "▲": "^", "▼": "v", "▬": "-", "█": "#", "▌": "|",
            "▐": "|", "▀": "-", "▄": "-", "▔": "-", "▁": "-",
            "": " ", "\u200b": "", "\ufeff": "",
        }
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        # Eliminar cualquier otro carácter no ASCII que no sea imprimible
        cleaned = ''.join(c if ord(c) < 128 or c in 'áéíóúñüÁÉÍÓÚÑÜ¿¡' else ' ' for c in cleaned)
        cleaned = cleaned.strip()
        if not cleaned:
            continue

        # Renderizar según formato
        if cleaned.startswith("# "):
            story.append(Paragraph(cleaned[2:], styles["Heading1"]))
        elif cleaned.startswith("## "):
            story.append(Paragraph(cleaned[3:], styles["Heading2"]))
        elif cleaned.startswith("### "):
            story.append(Paragraph(cleaned[4:], styles["Heading3"]))
        elif cleaned.startswith("- ") or cleaned.startswith("* "):
            story.append(Paragraph(f"  {cleaned[2:]}", body_style))
        elif cleaned.startswith("|") and cleaned.count("|") >= 3:
            # Detectar tabla
            cells = [c.strip() for c in cleaned.split("|") if c.strip()]
            if cells and not all(c.startswith("-") for c in cells if len(c) > 0):
                # Es una fila de tabla
                header = " | ".join(cells)
                story.append(Paragraph(f"<b>{header}</b>" if not any(c.isdigit() for c in cleaned.split("|")[1] if c.strip()) else header, body_style))
            else:
                story.append(Spacer(1, 0.1*cm))
        else:
            story.append(Paragraph(cleaned, body_style))

    # ── Pie de página ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_PURPLE))
    footer_style = ParagraphStyle(
        "footer", fontSize=7, textColor=COLOR_GRAY_TEXT, alignment=TA_CENTER,
    )
    story.append(Paragraph(
        f"AuditAI Pro — ISO 19011:2018 + ISO 23894:2023 · {datetime.now().strftime('%d/%m/%Y %H:%M')} · "
        f"Documento confidencial para uso interno de la organización.",
        footer_style,
    ))

    doc.build(story)
    return buffer.getvalue()


def generar_pdf(
    resultado: str,
    nombre_doc: str,
    usuario: str,
    proveedor: str,
    modelo: str,
    stats: dict,
) -> bytes:
    """Genera un PDF del reporte y devuelve los bytes."""
    if not _REPORTLAB_OK:
        return _pdf_sin_reportlab("gap_analysis")
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"Gap Analysis ISO 27001 — {nombre_doc}",
        author="Auditor ISO/IEC 27001:2022 IA",
    )

    styles = getSampleStyleSheet()
    story = []

    # ── Encabezado ────────────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        fontSize=20, textColor=COLOR_PURPLE,
        spaceAfter=4, alignment=TA_CENTER,
    )
    sub_style = ParagraphStyle(
        "Sub", parent=styles["Normal"],
        fontSize=10, textColor=COLOR_GRAY_TEXT,
        alignment=TA_CENTER, spaceAfter=2,
    )
    story.append(Paragraph("🔐 Gap Analysis ISO/IEC 27001:2022", title_style))
    story.append(Paragraph("Informe de Cumplimiento — Generado por IA Auditora", sub_style))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_PURPLE, spaceAfter=12))

    # ── Metadatos ─────────────────────────────────────────────────────────────
    meta_data = [
        ["Documento analizado:", nombre_doc],
        ["Auditor (usuario):", usuario],
        ["Modelo de IA:", f"{proveedor} / {modelo}"],
        ["Fecha de análisis:", datetime.now().strftime("%d/%m/%Y %H:%M UTC")],
        ["Estándar evaluado:", "ISO/IEC 27001:2022 — Anexo A"],
    ]
    meta_style = ParagraphStyle("meta", fontSize=9, leading=14)
    meta_table = Table(meta_data, colWidths=[5*cm, 11*cm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), COLOR_DARK),
        ("TEXTCOLOR", (1, 0), (1, -1), COLOR_GRAY_TEXT),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_GRAY_BG),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Resumen ejecutivo ─────────────────────────────────────────────────────
    section_style = ParagraphStyle(
        "Section", fontSize=12, textColor=COLOR_PURPLE,
        fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6,
    )
    story.append(Paragraph("Resumen Ejecutivo de Cumplimiento", section_style))

    conformes     = stats.get("conformes", 0)
    parciales     = stats.get("parciales", 0)
    no_conformes  = stats.get("no_conformes", 0)
    pct           = stats.get("cumplimiento_pct", 0.0)
    total         = conformes + parciales + no_conformes or 1

    # Barra de progreso visual simple
    barra_llena   = int(pct / 5)  # bloques de 5%
    barra_vacia   = 20 - barra_llena
    barra         = "█" * barra_llena + "░" * barra_vacia

    resumen_data = [
        ["Indicador", "Valor", "Porcentaje"],
        ["✅ Controles CONFORMES",   str(conformes),    f"{conformes/total*100:.0f}%"],
        ["⚠️  Controles PARCIALES",  str(parciales),    f"{parciales/total*100:.0f}%"],
        ["❌ Controles NO CONFORMES", str(no_conformes), f"{no_conformes/total*100:.0f}%"],
        ["📊 Cumplimiento estimado", f"{pct}%",         barra],
    ]
    resumen_table = Table(resumen_data, colWidths=[8*cm, 3*cm, 5*cm])
    resumen_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), COLOR_PURPLE),
        ("TEXTCOLOR",     (0, 0), (-1, 0), COLOR_WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ALIGN",         (1, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ("TEXTCOLOR",     (0, 1), (0, 1), COLOR_GREEN),
        ("TEXTCOLOR",     (0, 2), (0, 2), COLOR_YELLOW),
        ("TEXTCOLOR",     (0, 3), (0, 3), COLOR_RED),
        ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
    ]))
    story.append(resumen_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Tabla de Gap Analysis ─────────────────────────────────────────────────
    story.append(Paragraph("Tabla Detallada de Gap Analysis", section_style))

    headers, rows = _parse_md_table(resultado)

    if headers and rows:
        import html
        
        # Estilos para las celdas
        header_style = ParagraphStyle("th", fontSize=8, fontName="Helvetica-Bold", textColor=COLOR_WHITE)
        cell_style = ParagraphStyle("td", fontSize=8, fontName="Helvetica", leading=10, wordWrap='CJK')
        
        # Limpiar emojis de cabeceras para PDF y convertirlas a Paragraph
        clean_headers = [Paragraph(html.escape(re.sub(r'[✅⚠️❌📋🔐]', '', h).strip()).replace("**", ""), header_style) for h in headers]
        
        # Convertir celdas a Paragraph
        formatted_rows = []
        for row in rows:
            formatted_row = []
            for j, cell in enumerate(row):
                # Limpiar markdown y escapar HTML para que ReportLab no rompa el XML
                clean_cell = html.escape(cell).replace("**", "")
                
                # Colorear la columna de estado (índice 1)
                if j == 1:
                    color_hex = _estado_color(cell).hexval()[2:] # Quita el '0x'
                    color_str = f"#{color_hex}" if not color_hex.startswith('#') else color_hex
                    if len(color_str) == 7: # e.g. #059669
                         cell_content = f"<font color='{color_str}'><b>{clean_cell}</b></font>"
                    else:
                         cell_content = f"<b>{clean_cell}</b>"
                    formatted_row.append(Paragraph(cell_content, cell_style))
                else:
                    formatted_row.append(Paragraph(clean_cell, cell_style))
            formatted_rows.append(formatted_row)
            
        table_data = [clean_headers] + formatted_rows

        # Anchos de columna según número de columnas (A4 usable width = 17cm)
        if len(headers) == 3:
            col_widths = [4.5*cm, 4.0*cm, 8.5*cm]
        else:
            col_widths = None

        gap_table = Table(table_data, colWidths=col_widths, repeatRows=1)

        ts = [
            ("BACKGROUND",    (0, 0), (-1, 0), COLOR_DARK),
            ("TEXTCOLOR",     (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8),
            ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("WORDWRAP",      (0, 0), (-1, -1), True),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
            ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#e2e8f0")),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ]
        # Colorear filas por estado
        for i, row in enumerate(rows, start=1):
            if len(row) > 1:
                estado = row[1]
                c = _estado_color(estado)
                ts.append(("TEXTCOLOR", (1, i), (1, i), c))
                ts.append(("FONTNAME",  (1, i), (1, i), "Helvetica-Bold"))

        gap_table.setStyle(TableStyle(ts))
        story.append(gap_table)
    else:
        # Fallback: texto plano
        body_style = ParagraphStyle("body", fontSize=8, leading=12, spaceAfter=4)
        for line in resultado.splitlines():
            if line.strip():
                story.append(Paragraph(line.strip(), body_style))

    # ── Pie de página ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_PURPLE))
    footer_style = ParagraphStyle(
        "footer", fontSize=7, textColor=COLOR_GRAY_TEXT, alignment=TA_CENTER,
    )
    story.append(Paragraph(
        f"Generado por Auditor ISO/IEC 27001:2022 IA · {datetime.now().strftime('%d/%m/%Y %H:%M')} · "
        f"Este reporte no reemplaza una auditoría formal certificada.",
        footer_style,
    ))

    doc.build(story)
    return buffer.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# Formato profesional de Informe de Auditoría ISO 27001
# Basado en estructura de informes ISO 19011
# ══════════════════════════════════════════════════════════════════════════════

def generar_informe_auditoria_profesional(
    resultado_md: str,
    nombre_empresa: str,
    sector: str,
    tamano_empresa: str,
    nombre_doc: str,
    usuario: str,
    proveedor: str,
    modelo: str,
    stats: dict,
    controles_seleccionados: list[dict] | None = None,
    plan_implementacion: dict | None = None,
) -> bytes:
    if not _REPORTLAB_OK:
        return _pdf_sin_reportlab("informe_auditoria_profesional")
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        title=f"Informe de Auditoría ISO 27001 — {nombre_empresa or nombre_doc}",
        author=f"Auditor: {usuario}",
    )

    styles = getSampleStyleSheet()
    story = []

    # ── PORTADA ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*cm))
    title_cover = ParagraphStyle("TitleCover", fontSize=26, textColor=COLOR_DARK,
                                 fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=6)
    story.append(Paragraph("INFORME DE AUDITORÍA", title_cover))
    story.append(Paragraph("ISO/IEC 27001:2022", title_cover))
    sub_cover = ParagraphStyle("SubCover", fontSize=13, textColor=COLOR_PURPLE,
                               fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4)
    story.append(Paragraph("Sistema de Gestión de Seguridad de la Información", sub_cover))
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="60%", thickness=2, color=COLOR_PURPLE, spaceAfter=12))
    story.append(Spacer(1, 1*cm))

    cm_s = ParagraphStyle("cm", fontSize=11, fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4)
    if nombre_empresa:
        story.append(Paragraph(f"<b>Organización:</b> {nombre_empresa}", cm_s))
    if sector:
        story.append(Paragraph(f"<b>Sector:</b> {sector} ({tamano_empresa})", cm_s))
    story.append(Paragraph(f"<b>Documento auditado:</b> {nombre_doc}", cm_s))
    story.append(Paragraph(f"<b>Auditor:</b> {usuario}", cm_s))
    story.append(Paragraph(f"<b>Fecha de emisión:</b> {datetime.now().strftime('%d/%m/%Y %H:%M UTC')}", cm_s))
    story.append(Paragraph(f"<b>Modelo de IA:</b> {proveedor} / {modelo}", cm_s))
    story.append(Spacer(1, 1.5*cm))
    conf_s = ParagraphStyle("conf", fontSize=9, textColor=COLOR_RED, fontName="Helvetica-Bold", alignment=TA_CENTER)
    story.append(Paragraph("CONFIDENCIAL — Solo para uso interno de la organización", conf_s))
    story.append(Paragraph("Este informe contiene información sensible de seguridad de la información",
                           ParagraphStyle("conf2", fontSize=8, textColor=COLOR_GRAY_TEXT, alignment=TA_CENTER)))
    story.append(Spacer(1, 2*cm))
    doc.build(story)
    story.clear()

    # ── RESUMEN EJECUTIVO ─────────────────────────────────────────────────────
    section_s = ParagraphStyle("Sec", fontSize=14, textColor=COLOR_DARK,
                               fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6)

    story.append(Paragraph("1. Resumen Ejecutivo", section_s))
    conformes = stats.get("conformes", 0)
    parciales = stats.get("parciales", 0)
    no_conformes = stats.get("no_conformes", 0)
    pct = stats.get("cumplimiento_pct", 0.0)
    total = conformes + parciales + no_conformes or 1

    resumen_texto = (
        f"Se realizó una auditoría de brechas sobre la política de seguridad de la información "
        f"de <b>{nombre_empresa or nombre_doc}</b>, evaluando <b>{total}</b> controles del Anexo A de "
        f"ISO/IEC 27001:2022. El nivel de cumplimiento estimado es del <b>{pct:.1f}%</b>. "
        f"Se identificaron <b>{no_conformes}</b> controles no conformes, <b>{parciales}</b> parciales "
        f"y <b>{conformes}</b> conformes."
    )
    body_s = ParagraphStyle("Body", fontSize=10, fontName="Helvetica", leading=14, spaceAfter=8)
    story.append(Paragraph(resumen_texto, body_s))

    barra_llena = int(pct / 5)
    barra = "█" * barra_llena + "░" * (20 - barra_llena)
    res_data = [
        ["Indicador", "Cantidad", "%", "Barra"],
        ["✅ Conformes",   str(conformes),    f"{conformes/total*100:.0f}%", ""],
        ["⚠️ Parciales",   str(parciales),    f"{parciales/total*100:.0f}%", ""],
        ["❌ No conformes", str(no_conformes), f"{no_conformes/total*100:.0f}%", ""],
        ["📊 Cumplimiento", "", f"{pct:.1f}%", barra],
    ]
    rt = Table(res_data, colWidths=[6*cm, 3*cm, 3*cm, 5*cm])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ("TEXTCOLOR", (0, 1), (0, 1), COLOR_GREEN),
        ("TEXTCOLOR", (0, 2), (0, 2), COLOR_YELLOW),
        ("TEXTCOLOR", (0, 3), (0, 3), COLOR_RED),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.5*cm))

    # ── ALCANCE ────────────────────────────────────────────────────────────────
    story.append(Paragraph("2. Alcance y Metodología", section_s))
    alc_data = [
        ["Elemento", "Descripción"],
        ["Estándar", "ISO/IEC 27001:2022 — Anexo A"],
        ["Norma de auditoría", "ISO 19011:2018"],
        ["Alcance", f"Análisis de brechas de {nombre_empresa or nombre_doc}"],
        ["Metodología", "Evaluación automatizada por IA con fuentes normativas"],
        ["Sector", sector or "—"],
        ["Tamaño", tamano_empresa or "—"],
        ["Controles", f"{total} del Anexo A"],
        ["Fecha", datetime.now().strftime("%d/%m/%Y")],
    ]
    at = Table(alc_data, colWidths=[5*cm, 12*cm])
    at.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(at)
    story.append(Spacer(1, 0.5*cm))

    # ── RESULTADOS ─────────────────────────────────────────────────────────────
    story.append(Paragraph("3. Resultados del Gap Analysis", section_s))
    headers, rows = _parse_md_table(resultado_md)
    if headers and rows:
        import html
        h_s = ParagraphStyle("h", fontSize=8, fontName="Helvetica-Bold", textColor=COLOR_WHITE)
        c_s = ParagraphStyle("c", fontSize=8, fontName="Helvetica", leading=10, wordWrap='CJK')
        clean_h = [Paragraph(html.escape(re.sub(r'[✅⚠️❌📋🔐]', '', h).strip()).replace("**", ""), h_s) for h in headers]
        f_rows = []
        for row in rows:
            fr = []
            for j, cell in enumerate(row):
                clean_c = html.escape(cell).replace("**", "")
                if j == 1:
                    chex = _estado_color(cell).hexval()[2:]
                    cstr = f"#{chex}" if not chex.startswith('#') else chex
                    fr.append(Paragraph(f"<font color='{cstr}'><b>{clean_c}</b></font>", c_s))
                else:
                    fr.append(Paragraph(clean_c, c_s))
            f_rows.append(fr)
        td = [clean_h] + f_rows
        cw = [4.5*cm, 4.0*cm, 8.5*cm] if len(headers) == 3 else None
        gt = Table(td, colWidths=cw, repeatRows=1)
        ts = [
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
        ]
        for i, row in enumerate(rows, start=1):
            if len(row) > 1:
                c = _estado_color(row[1])
                ts.append(("TEXTCOLOR", (1, i), (1, i), c))
                ts.append(("FONTNAME", (1, i), (1, i), "Helvetica-Bold"))
        gt.setStyle(TableStyle(ts))
        story.append(gt)
    else:
        bs = ParagraphStyle("b", fontSize=8, leading=12, spaceAfter=4)
        for line in resultado_md.splitlines():
            if line.strip():
                story.append(Paragraph(line.strip(), bs))
    story.append(Spacer(1, 0.5*cm))

    # ── CONTROLES ──────────────────────────────────────────────────────────────
    if controles_seleccionados:
        story.append(Paragraph("4. Controles Recomendados", section_s))
        cd = [["Control", "Nombre", "Prioridad", "Tiempo", "Estado"]]
        for c in controles_seleccionados:
            icon_p = {"alta": "🔴", "media": "🟡", "baja": "🟢"}.get(c.get("prioridad", ""), "⚪")
            cd.append([c.get("id", ""), c.get("nombre", ""), f"{icon_p} {c.get('prioridad','').upper()}", c.get("tiempo_estimado",""), c.get("estado","pendiente")])
        ct = Table(cd, colWidths=[3*cm, 6*cm, 3*cm, 3*cm, 3*cm])
        ct.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(ct)
        story.append(Spacer(1, 0.5*cm))

    # ── PLAN ───────────────────────────────────────────────────────────────────
    if plan_implementacion:
        story.append(Paragraph("5. Plan de Implementación", section_s))
        for fase in plan_implementacion.get("fases", []):
            fs = ParagraphStyle("f", fontSize=10, fontName="Helvetica-Bold", textColor=COLOR_PURPLE, spaceBefore=8, spaceAfter=4)
            story.append(Paragraph(f"<b>{fase.get('fase','')}</b> — {fase.get('duracion_estimada','')}", fs))
            items = fase.get("controles", [])
            if items:
                fd = [["Control", "Nombre", "Prioridad", "Tiempo", "Responsable"]]
                for it in items:
                    fd.append([it.get("id",""), it.get("nombre",""), it.get("prioridad",""), it.get("tiempo_estimado",""), it.get("responsable_sugerido","TI")])
                ft = Table(fd, colWidths=[3*cm, 5*cm, 2.5*cm, 3*cm, 4*cm])
                ft.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), COLOR_PURPLE),
                    ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_GRAY_BG, COLOR_WHITE]),
                    ("GRID", (0, 0), (-1, -1), 0.2, colors.HexColor("#cbd5e1")),
                ]))
                story.append(ft)
                story.append(Spacer(1, 0.2*cm))

    # ── CONCLUSIONES ───────────────────────────────────────────────────────────
    story.append(Paragraph("6. Conclusiones y Recomendaciones", section_s))
    conclusion_text = (
        f"Basado en la evaluación, el nivel de cumplimiento de <b>{nombre_empresa or nombre_doc}</b> "
        f"frente a los requisitos del Anexo A de ISO/IEC 27001:2022 es del <b>{pct:.1f}%</b>. "
    )
    if pct >= 80:
        conclusion_text += "La organización tiene un nivel de madurez aceptable."
    elif pct >= 50:
        conclusion_text += "Existen brechas significativas que requieren atención inmediata."
    else:
        conclusion_text += "El nivel es bajo. Se recomienda un plan de acción integral."
    story.append(Paragraph(conclusion_text, body_s))
    story.append(Paragraph("<b>Recomendaciones principales:</b>", ParagraphStyle("r", fontSize=10, fontName="Helvetica-Bold", spaceBefore=8)))
    recs = [
        "Priorizar los controles no conformes con acciones correctivas inmediatas.",
        "Asignar responsables y plazos para cada control.",
        "Realizar revisiones periódicas del progreso.",
        "Capacitar al personal en los nuevos controles.",
        "Documentar evidencias para futuras auditorías.",
    ]
    rs = ParagraphStyle("rs", fontSize=9, fontName="Helvetica", leading=12, leftIndent=10, spaceAfter=2)
    for r in recs:
        story.append(Paragraph(f"• {r}", rs))

    # ── FIRMA ──────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_PURPLE))
    story.append(Paragraph("7. Firma del Auditor", section_s))
    fs = ParagraphStyle("fs", fontSize=10, fontName="Helvetica", spaceBefore=4, spaceAfter=4)
    story.append(Paragraph(f"<b>Auditor:</b> {usuario}", fs))
    story.append(Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}", fs))
    story.append(Paragraph("<b>Firma:</b> ___________________________________", fs))

    ds = ParagraphStyle("ds", fontSize=8, textColor=COLOR_GRAY_TEXT, spaceBefore=8)
    story.append(Paragraph(
        f"<i>Generado con IA ({proveedor}). No reemplaza una auditoría formal certificada.</i>", ds))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_PURPLE, spaceBefore=6))
    fl = ParagraphStyle("fl", fontSize=7, textColor=COLOR_GRAY_TEXT, alignment=TA_CENTER)
    story.append(Paragraph(f"AuditAI Pro · ISO 27001:2022 · {datetime.now().strftime('%d/%m/%Y %H:%M')} · Confidencial", fl))

    doc.build(story)
    return buffer.getvalue()


def generar_plantilla_informe_markdown(
    nombre_empresa: str,
    sector: str,
    tamano_empresa: str,
    usuario: str,
    proveedor: str,
    modelo: str,
) -> str:
    return f"""# INFORME DE AUDITORÍA ISO/IEC 27001:2022

---

## 1. Información General

| Campo | Valor |
|-------|-------|
| **Organización** | {nombre_empresa or "[Nombre de la empresa]"} |
| **Sector** | {sector or "[Sector]"} |
| **Tamaño** | {tamano_empresa or "[Tamaño]"} |
| **Estándar evaluado** | ISO/IEC 27001:2022 — Anexo A |
| **Auditor** | {usuario} |
| **Fecha** | {datetime.now().strftime("%d/%m/%Y")} |
| **Modelo de IA** | {proveedor} / {modelo} |

---

## 2. Resumen Ejecutivo

*Ejemplo:* Se evaluaron XX controles del Anexo A. Se identificaron XX conformes, XX parciales y XX no conformes. Nivel de cumplimiento: XX%.

---

## 3. Alcance y Metodología

- **Norma:** ISO/IEC 27001:2022
- **Auditoría:** ISO 19011:2018
- **Metodología:** Gap Analysis asistido por IA
- **Documentos:** [listar]

---

## 4. Resultados del Gap Analysis

| Control ISO | Estado | Acción Correctiva |
|-------------|--------|-------------------|
| A.5.1 | ✅ Conforme | — |
| A.5.9 | ⚠️ Parcial | Completar inventario |
| A.5.15 | ❌ No conforme | Implementar control |

---

## 5. Controles Recomendados ISO 27002

| Control | Nombre | Prioridad | Tiempo | Responsable |
|---------|--------|-----------|--------|-------------|
| A.5.1 | Políticas | Alta | 2 sem. | TI |

---

## 6. Plan de Implementación

### Fase 1: Alta — 1-2 meses
| Control | Acción | Responsable | Plazo |
|---------|--------|-------------|-------|

### Fase 2: Media — 2-4 meses
...

### Fase 3: Baja — 3-6 meses
...

---

## 7. Conclusiones

**Recomendaciones:** [completar]

---

## 8. Firma

**Auditor:** _________________
**Fecha:** __________________
**Firma:** __________________

---

*Este informe no reemplaza una auditoría formal certificada.*
"""
