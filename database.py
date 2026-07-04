"""
Módulo de Historial de Reportes — SQLite
Almacena cada Gap Analysis ejecutado con sus metadatos y resultados.
"""
import sqlite3
import re
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Zona horaria Bogotá (UTC-5)
BOGOTA_OFFSET = timedelta(hours=-5)

def _ahora_bogota():
    return datetime.now(timezone.utc) + BOGOTA_OFFSET

DB_PATH = Path("data") / "reportes.db"
DB_PATH.parent.mkdir(exist_ok=True)


def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reportes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at  TEXT NOT NULL,
            usuario     TEXT NOT NULL,
            fuente      TEXT NOT NULL,
            nombre_doc  TEXT NOT NULL,
            proveedor   TEXT NOT NULL,
            modelo      TEXT NOT NULL,
            resultado   TEXT NOT NULL,
            conformes   INTEGER DEFAULT 0,
            parciales   INTEGER DEFAULT 0,
            no_conformes INTEGER DEFAULT 0,
            cumplimiento_pct REAL DEFAULT 0.0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vulnerabilidades_ia (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            id_vulnerabilidad   TEXT UNIQUE NOT NULL,
            created_at          TEXT NOT NULL,
            fuente_origen       TEXT NOT NULL,
            resumen_es          TEXT,
            descripcion_riesgo  TEXT,
            causa_raiz          TEXT,
            accion_remediacion  TEXT,
            tactica_mitre       TEXT,
            clasificacion_tipo  TEXT,
            probabilidad_base   INTEGER DEFAULT 3,
            severidad_tecnica   INTEGER DEFAULT 3,
            riesgo_valor        INTEGER DEFAULT 9,
            nivel_riesgo        TEXT DEFAULT 'MEDIO',
            criticidad          REAL DEFAULT 50.0,
            controles_nist      TEXT,
            normas_aplicables   TEXT,
            sistemas_afectados  TEXT,
            raw_json            TEXT,
            contexto_org        TEXT,
            activa              INTEGER DEFAULT 1,
            como_se_ejecuta     TEXT,
            como_prevenirlo     TEXT,
            normativa_colombia  TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_vuln_fuente ON vulnerabilidades_ia(fuente_origen)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_vuln_nivel ON vulnerabilidades_ia(nivel_riesgo)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_vuln_activa ON vulnerabilidades_ia(activa)
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS auditoria_progreso (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario             TEXT NOT NULL,
            sector              TEXT,
            tamano_empresa      TEXT,
            nombre_empresa      TEXT,
            etapa_actual        TEXT DEFAULT 'gap_analysis',
            fecha_inicio        TEXT NOT NULL,
            fecha_actualizacion TEXT NOT NULL,
            gap_analysis_id     INTEGER,
            controles_json      TEXT,
            plan_json           TEXT,
            estado_json         TEXT DEFAULT '{}'
        )
    """)
    conn.commit()
    conn.close()


def parsear_stats(resultado: str) -> dict:
    """Extrae conteos analizando la columna de estado de la tabla."""
    conformes = 0
    parciales = 0
    no_conformes = 0
    
    for line in resultado.splitlines():
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'Control ISO' in line:
            continue
        
        cells = [c.strip() for c in line.split('|') if c.strip() != ""]
        if len(cells) >= 2:
            estado = cells[1].upper()
            if "CONFORME" in estado and "NO" not in estado:
                conformes += 1
            elif "PARCIAL" in estado or "⚠️" in estado:
                parciales += 1
            elif "NO CONFORME" in estado or "❌" in estado:
                no_conformes += 1

    total = conformes + parciales + no_conformes
    pct = round((conformes + parciales * 0.5) / total * 100, 1) if total > 0 else 0.0
    return {
        "conformes": conformes,
        "parciales": parciales,
        "no_conformes": no_conformes,
        "cumplimiento_pct": pct,
    }


def guardar_reporte(usuario: str, fuente: str, nombre_doc: str,
                    proveedor: str, modelo: str, resultado: str):
    stats = parsear_stats(resultado)
    conn = get_conn()
    conn.execute("""
        INSERT INTO reportes
            (created_at, usuario, fuente, nombre_doc, proveedor, modelo,
             resultado, conformes, parciales, no_conformes, cumplimiento_pct)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        usuario, fuente, nombre_doc, proveedor, modelo, resultado,
        stats["conformes"], stats["parciales"], stats["no_conformes"],
        stats["cumplimiento_pct"],
    ))
    conn.commit()
    conn.close()
    return stats


def listar_reportes(limit: int = 50) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM reportes ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def obtener_reporte(reporte_id: int) -> dict | None:
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM reportes WHERE id = ?", (reporte_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def stats_globales() -> dict:
    conn = get_conn()
    row = conn.execute("""
        SELECT
            COUNT(*) as total_reportes,
            SUM(conformes) as total_conformes,
            SUM(parciales) as total_parciales,
            SUM(no_conformes) as total_no_conformes,
            AVG(cumplimiento_pct) as avg_cumplimiento,
            COUNT(DISTINCT usuario) as total_usuarios
        FROM reportes
    """).fetchone()
    conn.close()
    return dict(row) if row else {}


# ══════════════════════════════════════════════════════════════════════════════
# CRUD para Vulnerabilidades de IA (Matriz de Riesgos)
# ══════════════════════════════════════════════════════════════════════════════

def guardar_vulnerabilidad(vuln: dict) -> bool:
    """Inserta o actualiza una vulnerabilidad (UPSERT por id_vulnerabilidad)."""
    conn = get_conn()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO vulnerabilidades_ia
                (id_vulnerabilidad, created_at, fuente_origen, resumen_es,
                 descripcion_riesgo, causa_raiz, accion_remediacion,
                 tactica_mitre, clasificacion_tipo, probabilidad_base,
                 severidad_tecnica, riesgo_valor, nivel_riesgo, criticidad,
                 controles_nist, normas_aplicables, sistemas_afectados, raw_json, contexto_org,
                 como_se_ejecuta, como_prevenirlo, normativa_colombia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vuln.get("id_vulnerabilidad", "PENDIENTE"),
            vuln.get("created_at", _ahora_bogota().isoformat()),
            vuln.get("fuente_origen", ""),
            vuln.get("resumen_es", ""),
            vuln.get("descripcion_riesgo", ""),
            vuln.get("causa_raiz", ""),
            vuln.get("accion_remediacion", ""),
            vuln.get("tactica_mitre", ""),
            vuln.get("clasificacion_tipo", "Tecnico"),
            vuln.get("probabilidad_base", 3),
            vuln.get("severidad_tecnica", 3),
            vuln.get("riesgo_valor", vuln.get("probabilidad_base", 3) * vuln.get("severidad_tecnica", 3)),
            vuln.get("nivel_riesgo", "MEDIO"),
            vuln.get("criticidad", 50.0),
            vuln.get("controles_nist", ""),
            _safe_json(vuln.get("normas_aplicables", [])) if isinstance(vuln.get("normas_aplicables"), list) else str(vuln.get("normas_aplicables", "")),
            _safe_json(vuln.get("sistemas_afectados", [])) if isinstance(vuln.get("sistemas_afectados"), list) else str(vuln.get("sistemas_afectados", "")),
            _safe_json(vuln),
            vuln.get("contexto_org", ""),
            vuln.get("como_se_ejecuta", ""),
            vuln.get("como_prevenirlo", ""),
            _safe_json(vuln.get("normativa_colombia", [])),
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB] Error guardando vulnerabilidad {vuln.get('id_vulnerabilidad', '?')}: {e}")
        return False
    finally:
        conn.close()


class _JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return super().default(obj)


def _safe_json(obj) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False, cls=_JsonEncoder)
    except (TypeError, ValueError):
        return json.dumps(str(obj), ensure_ascii=False)


def guardar_lote_vulnerabilidades(vulnerabilidades: list[dict]) -> tuple[int, int]:
    """Guarda un lote de vulnerabilidades. Retorna (insertados, errores)."""
    insertados = 0
    errores = 0
    for v in vulnerabilidades:
        if guardar_vulnerabilidad(v):
            insertados += 1
        else:
            errores += 1
    return insertados, errores


def listar_vulnerabilidades(limit: int = 100, activa: bool = True) -> list[dict]:
    """Lista vulnerabilidades activas o todas."""
    conn = get_conn()
    if activa:
        rows = conn.execute(
            "SELECT * FROM vulnerabilidades_ia WHERE activa = 1 ORDER BY riesgo_valor DESC, created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM vulnerabilidades_ia ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        for field in ["normas_aplicables", "sistemas_afectados", "normativa_colombia"]:
            val = d.get(field)
            if val and isinstance(val, str):
                try:
                    d[field] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    d[field] = [val] if val else []
        result.append(d)
    return result


def obtener_vulnerabilidad(id_vulnerabilidad: str) -> dict | None:
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM vulnerabilidades_ia WHERE id_vulnerabilidad = ?",
        (id_vulnerabilidad,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def stats_vulnerabilidades() -> dict:
    """Estadísticas agregadas de la tabla de vulnerabilidades."""
    conn = get_conn()
    row = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN nivel_riesgo = 'EXTREMO' THEN 1 ELSE 0 END) as extremos,
            SUM(CASE WHEN nivel_riesgo = 'ALTO' THEN 1 ELSE 0 END) as altos,
            SUM(CASE WHEN nivel_riesgo = 'MEDIO' THEN 1 ELSE 0 END) as medios,
            SUM(CASE WHEN nivel_riesgo = 'BAJO' THEN 1 ELSE 0 END) as bajos,
            AVG(riesgo_valor) as riesgo_promedio,
            AVG(criticidad) as criticidad_promedio,
            COUNT(DISTINCT fuente_origen) as fuentes_distintas,
            MAX(created_at) as ultima_actualizacion
        FROM vulnerabilidades_ia WHERE activa = 1
    """).fetchone()
    conn.close()
    return dict(row) if row else {}


def desactivar_vulnerabilidad(id_vulnerabilidad: str) -> bool:
    """Marca una vulnerabilidad como inactiva (no la borra)."""
    conn = get_conn()
    conn.execute(
        "UPDATE vulnerabilidades_ia SET activa = 0 WHERE id_vulnerabilidad = ?",
        (id_vulnerabilidad,),
    )
    conn.commit()
    conn.close()
    return True


def limpiar_vulnerabilidades_antiguas(dias: int = 90) -> int:
    """Desactiva vulnerabilidades con más de N días de antigüedad."""
    conn = get_conn()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=dias)).isoformat()
    cursor = conn.execute(
        "UPDATE vulnerabilidades_ia SET activa = 0 WHERE created_at < ? AND activa = 1",
        (cutoff,),
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected


def exportar_excel_respaldo(vulnerabilidades: list[dict] | None = None) -> str:
    ...
    return str(ruta)


# ══════════════════════════════════════════════════════════════════════════════
# Ruta de Auditoría ISO 27002 — persistencia del progreso
# ══════════════════════════════════════════════════════════════════════════════

def crear_auditoria(usuario: str, sector: str = "", tamano_empresa: str = "",
                    nombre_empresa: str = "") -> int:
    ahora = _ahora_bogota().isoformat()
    conn = get_conn()
    cursor = conn.execute("""
        INSERT INTO auditoria_progreso
            (usuario, sector, tamano_empresa, nombre_empresa, etapa_actual,
             fecha_inicio, fecha_actualizacion, estado_json)
        VALUES (?, ?, ?, ?, 'gap_analysis', ?, ?, '{}')
    """, (usuario, sector, tamano_empresa, nombre_empresa, ahora, ahora))
    conn.commit()
    aid = cursor.lastrowid
    conn.close()
    return aid


def obtener_auditorias(usuario: str) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM auditoria_progreso WHERE usuario = ? ORDER BY id DESC",
        (usuario,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def obtener_auditoria(auditoria_id: int) -> dict | None:
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM auditoria_progreso WHERE id = ?",
        (auditoria_id,),
    ).fetchone()
    conn.close()
    if row:
        d = dict(row)
        for campo in ["controles_json", "plan_json", "estado_json"]:
            val = d.get(campo)
            if val and isinstance(val, str):
                try:
                    d[campo] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    d[campo] = {}
        return d
    return None


def actualizar_auditoria(auditoria_id: int, **kwargs):
    ahora = _ahora_bogota().isoformat()
    campos_permitidos = {"sector", "tamano_empresa", "nombre_empresa",
                         "etapa_actual", "gap_analysis_id",
                         "controles_json", "plan_json", "estado_json"}
    sets = []
    valores = []
    for k, v in kwargs.items():
        if k in campos_permitidos:
            if k in ("controles_json", "plan_json", "estado_json"):
                v = json.dumps(v, ensure_ascii=False)
            sets.append(f"{k} = ?")
            valores.append(v)
    if not sets:
        return
    sets.append("fecha_actualizacion = ?")
    valores.append(ahora)
    valores.append(auditoria_id)
    conn = get_conn()
    conn.execute(
        f"UPDATE auditoria_progreso SET {', '.join(sets)} WHERE id = ?",
        valores,
    )
    conn.commit()
    conn.close()
