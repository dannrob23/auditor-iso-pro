"""
Módulo de Auditoría de Eventos — ISO/IEC 27001:2022 Control A.8.15
Registra: quién, qué acción, cuándo, desde dónde, con qué resultado.
"""
import logging
import json
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "audit.log"

# Formato estructurado JSON para cada evento
class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "event": record.getMessage(),
            "user": getattr(record, "user", "anonymous"),
            "action": getattr(record, "action", "unknown"),
            "ip": getattr(record, "ip", "localhost"),
            "result": getattr(record, "result", ""),
            "detail": getattr(record, "detail", ""),
        }, ensure_ascii=False)

def get_logger():
    logger = logging.getLogger("audit")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # Handler a archivo
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(JSONFormatter())
        logger.addHandler(fh)
    return logger

def log_event(action: str, user: str = "anonymous", result: str = "success", detail: str = ""):
    logger = get_logger()
    extra = {"user": user, "action": action, "ip": "localhost", "result": result, "detail": detail}
    if result == "success":
        logger.info(action, extra=extra)
    else:
        logger.warning(action, extra=extra)

def get_log_entries(n: int = 100) -> list[dict]:
    """Lee las últimas n entradas del log."""
    if not LOG_FILE.exists():
        return []
    entries = []
    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries[-n:]
