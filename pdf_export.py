"""
Módulo de exportación a PDF — Reportes de Gap Analysis ISO/IEC 27001:2022
Utiliza ReportLab para generar reportes profesionales.
"""
import io
import re
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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
    story.append(Paragraph("🧩 Propuesta de Implementación IA-SEC", title_style))
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
        ["✅ Cumplimiento total", str(c_total), f"{c_total/total_eval*100:.1f}%"],
        ["🟢 Mayormente implementado", str(c_mayor), f"{c_mayor/total_eval*100:.1f}%"],
        ["🟡 Implementado parcialmente", str(c_parcial), f"{c_parcial/total_eval*100:.1f}%"],
        ["🟠 En proceso inicial", str(c_inicial), f"{c_inicial/total_eval*100:.1f}%"],
        ["❌ No iniciado", str(c_no), f"{c_no/total_eval*100:.1f}%"],
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
    for line in propuesta.splitlines():
        if line.strip():
            # Convertir headers Markdown a estilos
            if line.startswith("# "):
                story.append(Paragraph(line[2:], styles["Heading1"]))
            elif line.startswith("## "):
                story.append(Paragraph(line[3:], styles["Heading2"]))
            elif line.startswith("### "):
                story.append(Paragraph(line[4:], styles["Heading3"]))
            elif line.startswith("- ") or line.startswith("* "):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            elif "|" in line and not line.startswith("|"):
                # Tabla simple
                story.append(Paragraph(line, body_style))
            else:
                story.append(Paragraph(line, body_style))
        else:
            story.append(Spacer(1, 0.2*cm))

    # ── Pie de página ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_PURPLE))
    footer_style = ParagraphStyle(
        "footer", fontSize=7, textColor=COLOR_GRAY_TEXT, alignment=TA_CENTER,
    )
    story.append(Paragraph(
        f"Generado por IA-SEC Auditor Tool · ISO 19011:2018 + ISO 23894:2023 · {datetime.now().strftime('%d/%m/%Y %H:%M')} · "
        f"Este documento es confidencial y para uso interno de la organización.",
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
