import math


# ── Matriz de Riesgo 5x5 (ISO 31000 / ISO 27005 / ISO 23894) ────────────────
# Probabilidad (1=Muy Baja ... 5=Muy Alta)
# Severidad/Impacto (1=Muy Bajo ... 5=Muy Alto)
# Riesgo = Probabilidad × Severidad → Escala 1-25

RISK_MATRIX_5X5: dict[tuple[int, int], str] = {}

for p in range(1, 6):
    for s in range(1, 6):
        v = p * s
        if v >= 20:
            RISK_MATRIX_5X5[(p, s)] = "EXTREMO"
        elif v >= 12:
            RISK_MATRIX_5X5[(p, s)] = "ALTO"
        elif v >= 6:
            RISK_MATRIX_5X5[(p, s)] = "MEDIO"
        else:
            RISK_MATRIX_5X5[(p, s)] = "BAJO"

COLOR_MAPA = {
    "EXTREMO": ("FF0000", "FFFFFF"),
    "ALTO":    ("FF6600", "000000"),
    "MEDIO":   ("FFD700", "000000"),
    "BAJO":    ("92D050", "000000"),
}


# ── Tácticas MITRE ATLAS ─────────────────────────────────────────────────────

TACTICAS_MITRE_ATLAS = {
    "AML.T0001": "Reconocimiento de sistemas de IA",
    "AML.T0002": "Reconocimiento del modelo ML",
    "AML.T0010": "ML Supply Chain Compromise",
    "AML.T0011": "Compromiso de datos de entrenamiento",
    "AML.T0012": "Modelo de acceso público para reutilización",
    "AML.T0013": "Adquisición de datos de terceros",
    "AML.T0014": "Recolección de datos del usuario",
    "AML.T0015": "Web scraping",
    "AML.T0016": "Cosecha de datos de repositorios públicos",
    "AML.T0017": "Ataque a la cadena de suministro de ML",
    "AML.T0018": "Backdoor ML",
    "AML.T0020": "Data Poisoning",
    "AML.T0021": "Model Poisoning",
    "AML.T0023": "Evasión de modelos de ML",
    "AML.T0024": "Adversarial Patch",
    "AML.T0025": "Ataque de caja negra",
    "AML.T0026": "Ataque de caja blanca",
    "AML.T0027": "Model Inversion",
    "AML.T0028": "Extracción de modelo",
    "AML.T0029": "Membership Inference",
    "AML.T0030": "Property Inference",
    "AML.T0031": "Model Stealing",
    "AML.T0032": "Data Exfiltration via ML Model",
    "AML.T0033": "Denial of Service (ML)",
    "AML.T0034": "ML Model Exhaustion",
    "AML.T0040": "Prompt Injection",
    "AML.T0041": "Indirect Prompt Injection",
    "AML.T0042": "Jailbreak de LLM",
    "AML.T0043": "Bias in AI Systems",
    "AML.T0044": "Model Skewing",
    "AML.T0045": "Concept Drift Exploitation",
    "AML.T0051": "Prompt Injection (LLM)",
    "AML.T0052": "Sesgo en modelos de lenguaje",
    "AML.T0053": "Generación de desinformación",
    "AML.T0054": "Deepfakes y suplantación",
    "AML.T0055": "Envenenamiento de RAG",
    "AML.T0056": "Ataque a embeddings",
}


def calcular_riesgo(probabilidad: int, severidad: int) -> dict:
    """
    Calcula el nivel de riesgo usando la matriz 5x5.
    Retorna: {valor, nivel, color, texto_color}
    """
    p = max(1, min(5, int(probabilidad)))
    s = max(1, min(5, int(severidad)))

    valor = p * s
    nivel = RISK_MATRIX_5X5.get((p, s), "BAJO")
    color, texto_color = COLOR_MAPA[nivel]

    return {
        "probabilidad_base": p,
        "severidad_tecnica": s,
        "riesgo_valor": valor,
        "nivel_riesgo": nivel,
        "color_hex": color,
        "texto_color": texto_color,
        "color_ahex": f"FF{color}",
    }


def clasificar_tactica(codigo: str) -> str:
    """Retorna el nombre descriptivo de una táctica MITRE ATLAS."""
    return TACTICAS_MITRE_ATLAS.get(codigo.upper().strip(), "AML.PENDIENTE - Sin clasificar")


def criticidad_compuesta(probabilidad: float, severidad: float) -> float:
    """
    Escala 0-100 para visualización rápida en dashboards.
    criticidad = ((probabilidad + severidad) / 10) * 100
    """
    p = max(1, min(5, probabilidad))
    s = max(1, min(5, severidad))
    return round(((p + s) / 10.0) * 100.0, 1)


def resumen_estadistico(vulnerabilidades: list[dict]) -> dict:
    """
    Agrupa vulnerabilidades por nivel de riesgo, fuente, clasificación.
    """
    stats = {
        "total": len(vulnerabilidades),
        "por_nivel": {"BAJO": 0, "MEDIO": 0, "ALTO": 0, "EXTREMO": 0},
        "por_fuente": {},
        "por_clasificacion": {},
        "criticidad_promedio": 0.0,
        "riesgo_promedio": 0.0,
    }

    suma_criticidad = 0.0
    suma_riesgo = 0.0

    for v in vulnerabilidades:
        p = v.get("probabilidad_base", 3)
        s = v.get("severidad_tecnica", 3)
        riesgo = calcular_riesgo(p, s)

        nivel = riesgo["nivel_riesgo"]
        stats["por_nivel"][nivel] = stats["por_nivel"].get(nivel, 0) + 1

        fuente = v.get("fuente_origen", "DESCONOCIDA")
        stats["por_fuente"][fuente] = stats["por_fuente"].get(fuente, 0) + 1

        clasif = v.get("clasificacion_tipo", "Tecnico")
        stats["por_clasificacion"][clasif] = stats["por_clasificacion"].get(clasif, 0) + 1

        suma_criticidad += criticidad_compuesta(p, s)
        suma_riesgo += riesgo["riesgo_valor"]

    if stats["total"] > 0:
        stats["criticidad_promedio"] = round(suma_criticidad / stats["total"], 1)
        stats["riesgo_promedio"] = round(suma_riesgo / stats["total"], 1)

    stats["color_global"] = (
        "#FF0000" if stats["por_nivel"].get("EXTREMO", 0) > 0 or stats["por_nivel"].get("ALTO", 0) > 2
        else "#FF6600" if stats["por_nivel"].get("ALTO", 0) > 0
        else "#FFD700" if stats["por_nivel"].get("MEDIO", 0) > 0
        else "#92D050"
    )
    return stats
