from typing import TypedDict, Optional


class StatsReporte(TypedDict):
    conformes: int
    parciales: int
    no_conformes: int
    cumplimiento_pct: float


class Reporte(TypedDict):
    id: int
    tenant_id: str
    created_at: str
    usuario: str
    fuente: str
    nombre_doc: str
    proveedor: str
    modelo: str
    resultado: str
    conformes: int
    parciales: int
    no_conformes: int
    cumplimiento_pct: float


class Vulnerabilidad(TypedDict):
    id_vulnerabilidad: str
    created_at: str
    fuente_origen: str
    resumen_es: str
    descripcion_riesgo: str
    causa_raiz: str
    accion_remediacion: str
    tactica_mitre: str
    clasificacion_tipo: str
    probabilidad_base: int
    severidad_tecnica: int
    riesgo_valor: int
    nivel_riesgo: str
    criticidad: float
    controles_nist: str
    normas_aplicables: str
    sistemas_afectados: str
    raw_json: str
    contexto_org: str
    activa: int
    como_se_ejecuta: str
    como_prevenirlo: str
    normativa_colombia: str


class StatsGlobales(TypedDict):
    total_reportes: int
    total_conformes: int
    total_parciales: int
    total_no_conformes: int
    avg_cumplimiento: float
    total_usuarios: int


class StatsVulnerabilidades(TypedDict):
    total: int
    extremos: int
    altos: int
    medios: int
    bajos: int
    riesgo_promedio: float
    criticidad_promedio: float
    fuentes_distintas: int
    ultima_actualizacion: str


class AuditoriaProgreso(TypedDict):
    id: int
    tenant_id: str
    usuario: str
    sector: str
    tamano_empresa: str
    nombre_empresa: str
    etapa_actual: str
    fecha_inicio: str
    fecha_actualizacion: str
    gap_analysis_id: Optional[int]
    controles_json: dict
    plan_json: dict
    estado_json: dict
