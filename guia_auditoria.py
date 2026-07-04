"""
Módulo Ruta de Auditoría ISO 27002
Guía al auditor desde el gap analysis hasta los controles finales,
adaptado a empresas de cualquier tamaño o sector (no solo infraestructura crítica).
"""
import json
from datetime import datetime, timezone, timedelta
from typing import Any

# ── Catálogo de etapas de la auditoría ───────────────────────────────────────
ETAPAS = [
    {
        "id": "gap_analysis",
        "nombre": "1. Gap Analysis",
        "descripcion": "Evaluación inicial del estado actual vs. requisitos ISO 27001",
        "icono": "🔍",
    },
    {
        "id": "identificar_brechas",
        "nombre": "2. Identificar Brechas",
        "descripcion": "Detectar controles ausentes o insuficientes del Anexo A",
        "icono": "⚠️",
    },
    {
        "id": "seleccionar_controles",
        "nombre": "3. Seleccionar Controles ISO 27002",
        "descripcion": "Elegir controles aplicables según sector y tamaño de la empresa",
        "icono": "🎯",
    },
    {
        "id": "plan_tratamiento",
        "nombre": "4. Plan de Tratamiento",
        "descripcion": "Priorizar acciones correctivas con plazos y responsables",
        "icono": "📋",
    },
    {
        "id": "implementacion",
        "nombre": "5. Implementación",
        "descripcion": "Ejecutar los controles seleccionados con seguimiento",
        "icono": "⚙️",
    },
    {
        "id": "seguimiento",
        "nombre": "6. Seguimiento y Mejora Continua",
        "descripcion": "Monitoreo periódico y auditoría interna de los controles implementados",
        "icono": "🔄",
    },
]

# ── Mapa de controles ISO 27002 priorizados por perfil de empresa ────────────
# Basado en ISO/IEC 27002:2022, Anexo A
_CONTROLES_27002 = [
    {
        "id": "A.5.1",
        "nombre": "Políticas de seguridad de la información",
        "categoria": "Gobernanza",
        "prioridad": {"PYME": "media", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "2 semanas", "mediana": "1 mes", "grande": "2 meses"},
        "descripcion": "Establecer, revisar y comunicar políticas de seguridad.",
    },
    {
        "id": "A.5.9",
        "nombre": "Inventario de activos",
        "categoria": "Identificación",
        "prioridad": {"PYME": "alta", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "1 semana", "mediana": "2 semanas", "grande": "1 mes"},
        "descripcion": "Identificar y registrar todos los activos de información.",
    },
    {
        "id": "A.5.15",
        "nombre": "Control de acceso",
        "categoria": "Protección",
        "prioridad": {"PYME": "alta", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "1 semana", "mediana": "2 semanas", "grande": "1 mes"},
        "descripcion": "Implementar políticas y mecanismos de control de acceso.",
    },
    {
        "id": "A.6.3",
        "nombre": "Concientización y formación",
        "categoria": "Personas",
        "prioridad": {"PYME": "alta", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "1 semana", "mediana": "2 semanas", "grande": "3 semanas"},
        "descripcion": "Capacitar al personal en seguridad de la información.",
    },
    {
        "id": "A.8.8",
        "nombre": "Gestión de vulnerabilidades técnicas",
        "categoria": "Tecnología",
        "prioridad": {"PYME": "media", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "2 semanas", "mediana": "1 mes", "grande": "2 meses"},
        "descripcion": "Establecer proceso de gestión de vulnerabilidades.",
    },
    {
        "id": "A.8.15",
        "nombre": "Registros y supervisión",
        "categoria": "Operaciones",
        "prioridad": {"PYME": "media", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "1 semana", "mediana": "2 semanas", "grande": "1 mes"},
        "descripcion": "Implementar logging y monitoreo de eventos de seguridad.",
    },
    {
        "id": "A.8.24",
        "nombre": "Criptografía",
        "categoria": "Protección",
        "prioridad": {"PYME": "baja", "mediana": "media", "grande": "alta"},
        "tiempo_estimado": {"PYME": "1 semana", "mediana": "2 semanas", "grande": "1 mes"},
        "descripcion": "Usar cifrado para proteger información sensible.",
    },
    {
        "id": "A.5.29",
        "nombre": "Seguridad en teletrabajo",
        "categoria": "Operaciones",
        "prioridad": {"PYME": "media", "mediana": "media", "grande": "alta"},
        "tiempo_estimado": {"PYME": "1 semana", "mediana": "2 semanas", "grande": "3 semanas"},
        "descripcion": "Políticas y controles para trabajo remoto.",
    },
    {
        "id": "A.8.10",
        "nombre": "Protección de datos personales",
        "categoria": "Privacidad",
        "prioridad": {"PYME": "alta", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "2 semanas", "mediana": "3 semanas", "grande": "2 meses"},
        "descripcion": "Cumplir con normativas de privacidad aplicables.",
    },
    {
        "id": "A.8.16",
        "nombre": "Gestión de incidentes",
        "categoria": "Operaciones",
        "prioridad": {"PYME": "alta", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "2 semanas", "mediana": "1 mes", "grande": "2 meses"},
        "descripcion": "Establecer proceso de respuesta a incidentes de seguridad.",
    },
    {
        "id": "A.8.25",
        "nombre": "Plan de continuidad del negocio",
        "categoria": "Continuidad",
        "prioridad": {"PYME": "media", "mediana": "alta", "grande": "alta"},
        "tiempo_estimado": {"PYME": "2 semanas", "mediana": "1 mes", "grande": "2 meses"},
        "descripcion": "Desarrollar y probar planes de continuidad.",
    },
    {
        "id": "A.5.22",
        "nombre": "Seguridad en la cadena de suministro",
        "categoria": "Terceros",
        "prioridad": {"PYME": "baja", "mediana": "media", "grande": "alta"},
        "tiempo_estimado": {"PYME": "1 mes", "mediana": "1 mes", "grande": "2 meses"},
        "descripcion": "Evaluar y gestionar riesgos de proveedores.",
    },
]

SECTORES_EMPRESA = [
    "Tecnología / Software",
    "Salud / Farmacéutico",
    "Financiero / Banca",
    "Comercio / Retail",
    "Educación",
    "Gobierno / Sector público",
    "Manufactura / Industrial",
    "Servicios profesionales",
    "Energía / Utilities",
    "Transporte / Logística",
    "Otro",
]

TAMANOS_EMPRESA = ["PYME (< 50 empleados)", "Mediana (50-250 empleados)", "Grande (> 250 empleados)"]


def _mapear_tamano(key: str) -> str:
    if key.startswith("PYME"):
        return "PYME"
    if key.startswith("Mediana"):
        return "mediana"
    return "grande"


def obtener_controles_recomendados(sector: str, tamano_empresa: str, brechas: list[str] | None = None) -> list[dict]:
    tam = _mapear_tamano(tamano_empresa)
    controles = []
    for ctrl in _CONTROLES_27002:
        prioridad = ctrl["prioridad"].get(tam, "media")
        # Si hay brechas, filtrar controles relacionados
        if brechas:
            coinciden = any(b.lower() in ctrl["nombre"].lower() or b.lower() in ctrl["id"].lower() for b in brechas)
            if not coinciden and prioridad == "baja":
                continue
        controles.append({
            "id": ctrl["id"],
            "nombre": ctrl["nombre"],
            "categoria": ctrl["categoria"],
            "prioridad": prioridad,
            "tiempo_estimado": ctrl["tiempo_estimado"].get(tam, "1 mes"),
            "descripcion": ctrl["descripcion"],
            "responsable_sugerido": "Responsable de seguridad / TI",
            "estado": "pendiente",
        })
    # ordenar por prioridad: alta -> media -> baja
    orden = {"alta": 0, "media": 1, "baja": 2}
    controles.sort(key=lambda c: orden.get(c["prioridad"], 99))
    return controles


def generar_plan_implementacion(controles: list[dict]) -> dict:
    plan = {
        "resumen": "",
        "fases": [],
        "total_controles": len(controles),
        "alta_prioridad": sum(1 for c in controles if c["prioridad"] == "alta"),
        "media_prioridad": sum(1 for c in controles if c["prioridad"] == "media"),
        "baja_prioridad": sum(1 for c in controles if c["prioridad"] == "baja"),
    }

    # Agrupar por prioridad
    fases = []
    for nivel in ("alta", "media", "baja"):
        ctrls = [c for c in controles if c["prioridad"] == nivel]
        if not ctrls:
            continue
        fases.append({
            "fase": f"Fase {len(fases) + 1}: Controles de prioridad {nivel.upper()}",
            "controles": ctrls,
            "duracion_estimada": "1-2 meses" if nivel == "alta" else (
                "2-4 meses" if nivel == "media" else "3-6 meses"
            ),
        })

    plan["fases"] = fases
    plan["resumen"] = (
        f"Plan de implementación con {plan['total_controles']} controles: "
        f"{plan['alta_prioridad']} de alta prioridad, "
        f"{plan['media_prioridad']} de media, "
        f"{plan['baja_prioridad']} de baja."
    )
    return plan


def generar_reporte_markdown(auditoria: dict, controles: list[dict], plan: dict,
                              nombre_empresa: str, sector: str, tamano_empresa: str) -> str:
    md = f"""# Plan de Implementación ISO 27002

## Información de la Empresa

| Campo | Valor |
|-------|-------|
| Nombre | {nombre_empresa or "No especificado"} |
| Sector | {sector or "No especificado"} |
| Tamaño | {tamano_empresa or "No especificado"} |

## Resumen del Plan

{plan.get('resumen', '')}

## Fases de Implementación

"""
    for fase in plan.get("fases", []):
        md += f"### {fase['fase']}\n\n"
        md += f"**Duración estimada:** {fase['duracion_estimada']}\n\n"
        md += "| Control | Nombre | Prioridad | Tiempo estimado | Responsable |\n"
        md += "|---------|--------|-----------|-----------------|-------------|\n"
        for ctrl in fase.get("controles", []):
            md += f"| {ctrl['id']} | {ctrl['nombre']} | {ctrl['prioridad']} | {ctrl['tiempo_estimado']} | {ctrl.get('responsable_sugerido', '')} |\n"
        md += "\n"

    md += "## Detalle por Control\n\n"
    for ctrl in controles:
        md += f"### {ctrl['id']}: {ctrl['nombre']}\n"
        md += f"- **Categoría:** {ctrl['categoria']}\n"
        md += f"- **Prioridad:** {ctrl['prioridad']}\n"
        md += f"- **Tiempo estimado:** {ctrl['tiempo_estimado']}\n"
        md += f"- **Descripción:** {ctrl['descripcion']}\n"
        md += f"- **Responsable sugerido:** {ctrl.get('responsable_sugerido', '')}\n"
        md += "\n"
    return md


# ── Manejo de estados de cada etapa ──────────────────────────────────────────

def etapa_icono_estado(etapa_id: str, auditoria: dict) -> str:
    estado = auditoria.get("estado_json", {})
    if isinstance(estado, str):
        try:
            estado = json.loads(estado)
        except (json.JSONDecodeError, TypeError):
            estado = {}
    etapa_actual = auditoria.get("etapa_actual", "gap_analysis")
    et = estado.get(etapa_id, {})
    completado = et.get("completado", False) if isinstance(et, dict) else False
    if completado:
        return "✅"
    if etapa_id == etapa_actual and completado:
        return "✅"
    if etapa_id == etapa_actual:
        return "⏳"
    # Etapas anteriores a la actual están completadas
    ids = [e["id"] for e in ETAPAS]
    try:
        idx_actual = ids.index(etapa_actual)
        idx_esta = ids.index(etapa_id)
        if idx_esta < idx_actual:
            return "✅"
    except ValueError:
        pass
    return "⬜"


def avanzar_etapa(auditoria: dict, etapa_id: str) -> dict:
    estado = auditoria.get("estado_json", {})
    if isinstance(estado, str):
        try:
            estado = json.loads(estado)
        except (json.JSONDecodeError, TypeError):
            estado = {}
    estado[etapa_id] = {"completado": True, "actualizado": datetime.now(timezone.utc).isoformat()}
    auditoria["estado_json"] = estado
    # Avanzar a siguiente etapa
    ids = [e["id"] for e in ETAPAS]
    try:
        idx = ids.index(etapa_id)
        if idx + 1 < len(ids):
            auditoria["etapa_actual"] = ids[idx + 1]
    except ValueError:
        pass
    return auditoria
