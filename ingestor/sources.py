import requests
import json
import yaml
import time
from datetime import datetime, timezone
from typing import Optional


HTTP_TIMEOUT = 30
HEADERS = {
    "User-Agent": "IA-SEC-Auditor/1.0 (Matriz de Riesgos IA; +https://github.com/auditor-iso)",
    "Accept": "application/json, text/plain, text/yaml",
}


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 1: MITRE ATLAS — vía GitHub raw YAML
# URL: https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml
# Contiene todas las tácticas, técnicas, y case-studies del framework MITRE ATLAS
# ══════════════════════════════════════════════════════════════════════════════

MITRE_ATLAS_YAML_URL = (
    "https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml"
)

# URL alternativa STIX para el Navigator (cubre más datos)
MITRE_ATLAS_STIX_URL = (
    "https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/atlas.json"
)


def fetch_mitre_atlas(limit: int = 50) -> list[dict]:
    """
    Descarga el feed completo de MITRE ATLAS (tácticas + técnicas + mitigaciones)
    desde el YAML oficial del repositorio GitHub.
    Retorna una lista plana de técnicas con metadatos enriquecidos.
    """
    try:
        resp = requests.get(MITRE_ATLAS_YAML_URL, headers=HEADERS, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        data = yaml.safe_load(resp.text)

        matrix = data.get("matrices", [{}])[0]
        tactics_map = {}
        for t in matrix.get("tactics", []):
            tactics_map[t["id"]] = t["name"]

        techniques = matrix.get("techniques", [])
        mitigations = matrix.get("mitigations", [])

        results = []
        for tech in techniques:
            tech_id = tech["id"]
            # Saltar sub-técnicas (tienen punto, ej AML.T0000.000)
            if "." in tech_id and tech_id.count(".") >= 2:
                continue

            tactic_ids = tech.get("tactics", [])
            tactic_names = [tactics_map.get(tid, tid) for tid in tactic_ids]
            primary_tactic = tactic_names[0] if tactic_names else "Uncategorized"

            results.append({
                "id": tech_id,
                "title": tech["name"],
                "description": tech.get("description", ""),
                "source": "MITRE ATLAS",
                "classification": tech_id,
                "mitre_tactic": f"{tech_id} - {tech['name']}",
                "tactic_id": tactic_ids[0] if tactic_ids else "AML.TA0000",
                "tactic_name": primary_tactic,
                "severity": 3,
                "likelihood": 3,
                "published_date": tech.get("created_date", "2021-01-01"),
                "modified_date": tech.get("modified_date", ""),
                "maturity": tech.get("maturity", "feasible"),
                "remediation": (
                    f"Implementar controles según MITRE ATLAS para {tech['name']}. "
                    f"Consultar https://atlas.mitre.org/techniques/{tech_id} para mitigaciones detalladas."
                ),
                "nist_controls": [
                    "NIST AI RMF 3.0 - MAP (Mapeo de riesgos)",
                    "NIST AI RMF 2.0 - GOVERN (Gobernanza)",
                    "ISO 42001:2023 A.7 - Controles de seguridad IA",
                    "ISO 23894:2023 5.5 - Robustez adversarial",
                ],
                "affected_systems": ["AI/ML Systems", "ML Pipelines", "AI Infrastructure"],
                "url": f"https://atlas.mitre.org/techniques/{tech_id}",
            })
        return results[:limit]

    except (requests.RequestException, json.JSONDecodeError, yaml.YAMLError) as e:
        print(f"[MITRE ATLAS YAML] Error: {e}. Intentando STIX...")
        return _fetch_mitre_stix_fallback(limit)


def _fetch_mitre_stix_fallback(limit: int) -> list[dict]:
    """Fallback: intenta descargar desde el feed STIX del Navigator."""
    try:
        resp = requests.get(MITRE_ATLAS_STIX_URL, headers=HEADERS, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        stix_data = resp.json()
        objects = stix_data.get("objects", [])

        results = []
        for obj in objects:
            if obj.get("type") != "attack-pattern":
                continue
            name = obj.get("name", "")
            desc = obj.get("description", "")
            obj_id = obj.get("id", "").split("--")[-1][:12]
            results.append({
                "id": f"AML-{obj_id}",
                "title": name,
                "description": desc,
                "source": "MITRE ATLAS (STIX)",
                "classification": obj_id,
                "mitre_tactic": name,
                "severity": 3,
                "likelihood": 3,
                "published_date": obj.get("created", ""),
                "remediation": "Consultar MITRE ATLAS para mitigaciones específicas.",
                "nist_controls": ["NIST AI RMF 3.0"],
                "affected_systems": ["AI/ML Systems"],
            })
        return results[:limit]
    except Exception as e:
        print(f"[MITRE ATLAS STIX] Fallback falló: {e}")
        return []


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 2: AVID (AI Vulnerability Database) — vía GitHub raw JSON
# URL: https://raw.githubusercontent.com/avidml/avid-db/main/vulnerabilities/
# Cada vulnerabilidad está en un archivo JSON individual por año
# ══════════════════════════════════════════════════════════════════════════════

AVID_BASE = "https://raw.githubusercontent.com/avidml/avid-db/main/vulnerabilities"
AVID_YEARS = ["2022", "2023", "2024", "2025", "2026"]

# Índice conocido de vulnerabilidades AVID (actualizado a mayo 2026)
AVID_KNOWN_IDS = {
    "2022": list(range(1, 14)),
    "2023": list(range(1, 21)),
    "2024": list(range(1, 11)),
}

_avid_cache: list[dict] | None = None


def fetch_avid_reports(limit: int = 10) -> list[dict]:
    """
    Consulta la base de datos AVID desde el repositorio GitHub oficial.
    Formato real: AVID-{YEAR}-V{NNN}.json
    """
    global _avid_cache
    if _avid_cache is not None:
        return _avid_cache[:limit]

    results = []
    for year, nums in AVID_KNOWN_IDS.items():
        for num in nums:
            avid_id = f"AVID-{year}-V{num:03d}"
            url = f"{AVID_BASE}/{year}/{avid_id}.json"
            try:
                resp = requests.get(url, headers=HEADERS, timeout=HTTP_TIMEOUT)
                if resp.status_code == 200:
                    data = resp.json()
                    results.append(_parse_avid_entry(data, avid_id))
            except (requests.RequestException, json.JSONDecodeError) as e:
                print(f"[AVID] Error descargando {avid_id}: {e}")
                continue

    if not results:
        print("[AVID] No se pudo obtener ninguna vulnerabilidad real del repositorio GitHub.")
        return []

    _avid_cache = results
    return results[:limit]


def _parse_avid_entry(data: dict, avid_id: str) -> dict:
    """Parsea una entrada AVID al formato común del sistema.
    Formato real: {
      data_type, data_version, metadata, affects, problemtype,
      description, references, reports, impact, published_date, ...
    }
    """
    metadata = data.get("metadata", {})
    problemtype = data.get("problemtype", {})
    desc_obj = data.get("description", {})
    impact = data.get("impact", {}).get("avid", {})
    affects = data.get("affects", {})

    title = problemtype.get("description", {}).get("value", avid_id) if isinstance(problemtype.get("description"), dict) else avid_id
    desc = desc_obj.get("value", "") if isinstance(desc_obj, dict) else str(desc_obj)

    risk_domains = impact.get("risk_domain", ["General"])
    sep_view = impact.get("sep_view", [])

    # Extraer artifacts afectados
    artifacts = [a.get("name", "") for a in affects.get("artifacts", [])]
    deployers = affects.get("deployer", [])

    published = data.get("published_date", "")

    severity = 3
    for sep in sep_view:
        if "fairness" in sep.lower():
            severity = 4
        elif "privacy" in sep.lower() or "security" in sep.lower():
            severity = 4
        elif "safety" in sep.lower():
            severity = 5

    classification = risk_domains[0] if risk_domains else "AI Risk"

    references = data.get("references", [])
    if isinstance(references, list):
        refs = "; ".join([r.get("url", r.get("label", "")) for r in references[:3]])
    else:
        refs = "AVID Database"

    return {
        "id": avid_id,
        "title": title[:200],
        "description": desc[:500],
        "source": "AVID",
        "classification": classification,
        "mitre_tactic": f"{classification} - {title[:60]}",
        "severity": severity,
        "likelihood": max(1, min(5, severity)),
        "published_date": published if published else "2024-01-01",
        "remediation": f"Ver reports en AVID. Referencias: {refs}",
        "nist_controls": "; ".join(sep_view) if sep_view else "NIST AI RMF",
        "affected_systems": artifacts + deployers,
        "url": f"https://avidml.org/database/{avid_id}",
    }


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 3: MIT AI Risk Repository — Google Sheets export público
# El repositorio está en Google Sheets, accesible vía CSV export
# ══════════════════════════════════════════════════════════════════════════════

# URL del CSV export de la hoja principal del AI Risk Repository
MIT_RISK_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "15LeHcpeuZC9txkvcaMoh3sUhkMvdMMry69xxXL46DT0"
    "/export?format=csv&gid=0"
)

MIT_RISK_DOMAINS = [
    "Discrimination & Toxicity",
    "Privacy & Security",
    "Misinformation",
    "Malicious Actors",
    "Human-Computer Interaction",
    "Socioeconomic & Environmental",
    "AI System Safety, Failures, & Limitations",
]

SEVERITY_BY_DOMAIN = {
    "Discrimination & Toxicity": 3,
    "Privacy & Security": 4,
    "Misinformation": 3,
    "Malicious Actors": 5,
    "Human-Computer Interaction": 2,
    "Socioeconomic & Environmental": 3,
    "AI System Safety, Failures, & Limitations": 4,
}

LIKELIHOOD_BY_DOMAIN = {
    "Discrimination & Toxicity": 4,
    "Privacy & Security": 4,
    "Misinformation": 5,
    "Malicious Actors": 3,
    "Human-Computer Interaction": 4,
    "Socioeconomic & Environmental": 3,
    "AI System Safety, Failures, & Limitations": 3,
}


def fetch_mit_risk_repo(limit: int = 10) -> list[dict]:
    """
    Consulta el MIT AI Risk Repository.
    Descarga el CSV export desde Google Sheets y parsea las filas.
    Fallback: usa datos curados desde la página web del repositorio.
    """
    try:
        import csv
        resp = requests.get(MIT_RISK_CSV_URL, headers=HEADERS, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        content = resp.text
        reader = csv.DictReader(content.splitlines())
        results = []
        for row in reader:
            risk_title = row.get("Risk Title", row.get("Risk", ""))
            risk_desc = row.get("Risk Description", row.get("Description", ""))
            domain = row.get("Domain", row.get("Category", ""))
            subdomain = row.get("Subdomain", row.get("Subcategory", ""))

            if not risk_title:
                continue

            domain_clean = domain.strip()
            sev = SEVERITY_BY_DOMAIN.get(domain_clean, 3)
            like = LIKELIHOOD_BY_DOMAIN.get(domain_clean, 3)

            results.append({
                "id": f"MIT-RISK-{len(results)+1:04d}",
                "title": risk_title[:200],
                "description": risk_desc[:500] if risk_desc else risk_title,
                "source": "MIT AI Risk Repository",
                "classification": f"domain:{domain_clean}/sub:{subdomain}",
                "mitre_tactic": domain_clean,
                "severity": sev,
                "likelihood": like,
                "published_date": row.get("Year", row.get("Date", "2024")),
                "remediation": (
                    f"Aplicar controles del dominio '{domain_clean}'. "
                    f"Consultar el AI Risk Repository para mitigaciones detalladas."
                    if not row.get("Mitigation")
                    else row["Mitigation"]
                ),
                "nist_controls": f"NIST AI RMF - {domain_clean}",
                "affected_systems": ["AI Systems", "ML Applications"],
                "url": "https://airisk.mit.edu",
            })
            if len(results) >= limit:
                break
        return results

    except Exception as e:
        print(f"[MIT Risk CSV] Error: {e}. Usando datos curados de la web.")
        return _curated_mit_risks(limit)


def _curated_mit_risks(limit: int) -> list[dict]:
    """
    Datos curados desde la taxonomía oficial del MIT AI Risk Repository
    (7 dominios, 24 subdominios) publicada en airisk.mit.edu.
    Estos NO son mock — son risks reales categorizados por el equipo del MIT.
    """
    curated = [
        {
            "id": "MIT-RISK-D001",
            "title": "Unfair discrimination and misrepresentation by AI systems",
            "description": "AI systems producing unfair outcomes based on race, gender, or other sensitive characteristics, resulting in discriminatory treatment and misrepresentation of groups.",
            "domain": "Discrimination & Toxicity",
            "subdomain": "1.1 Unfair discrimination and misrepresentation",
        },
        {
            "id": "MIT-RISK-D002",
            "title": "AI exposure to toxic or harmful content",
            "description": "AI generating or exposing users to hate speech, violence, extremism, illegal acts, child sexual abuse material, or content violating community norms.",
            "domain": "Discrimination & Toxicity",
            "subdomain": "1.2 Exposure to toxic content",
        },
        {
            "id": "MIT-RISK-D003",
            "title": "Unequal AI performance across demographic groups",
            "description": "Accuracy and effectiveness of AI systems varies by group membership due to biased training data or design decisions, leading to unequal outcomes.",
            "domain": "Discrimination & Toxicity",
            "subdomain": "1.3 Unequal performance across groups",
        },
        {
            "id": "MIT-RISK-P001",
            "title": "Privacy compromise via AI inference of sensitive information",
            "description": "AI systems memorizing and leaking sensitive personal data, or inferring private information about individuals without consent, including identity theft risk.",
            "domain": "Privacy & Security",
            "subdomain": "2.1 Compromise of privacy",
        },
        {
            "id": "MIT-RISK-P002",
            "title": "AI system security vulnerabilities and adversarial attacks",
            "description": "Vulnerabilities in AI systems, ML pipelines, and hardware that can be exploited for unauthorized access, data breaches, or system manipulation.",
            "domain": "Privacy & Security",
            "subdomain": "2.2 AI system security vulnerabilities",
        },
        {
            "id": "MIT-RISK-M001",
            "title": "AI-generated false or misleading information",
            "description": "AI systems inadvertently generating or spreading false information, leading to inaccurate beliefs in users and undermining their autonomy.",
            "domain": "Misinformation",
            "subdomain": "3.1 False or misleading information",
        },
        {
            "id": "MIT-RISK-M002",
            "title": "Pollution of information ecosystem and loss of consensus reality",
            "description": "AI-generated misinformation creating filter bubbles, undermining shared reality, weakening social cohesion and democratic processes.",
            "domain": "Misinformation",
            "subdomain": "3.2 Pollution of information ecosystem",
        },
        {
            "id": "MIT-RISK-A001",
            "title": "AI-enabled disinformation and surveillance at scale",
            "description": "Large-scale AI disinformation campaigns, malicious surveillance, automated censorship, and propaganda to manipulate political processes and public opinion.",
            "domain": "Malicious Actors",
            "subdomain": "4.1 Disinformation, surveillance, and influence",
        },
        {
            "id": "MIT-RISK-A002",
            "title": "AI-powered fraud, scams, and targeted manipulation",
            "description": "Using AI for plagiarism, impersonation, financial scams, blackmail, or creating non-consensual intimate imagery for manipulation or extortion.",
            "domain": "Malicious Actors",
            "subdomain": "4.2 Fraud, scams, and targeted manipulation",
        },
        {
            "id": "MIT-RISK-A003",
            "title": "AI-enabled cyberattacks and weapons development",
            "description": "Using AI to develop more effective malware, cyber weapons, lethal autonomous weapons, or CBRNE weapons capable of causing mass harm.",
            "domain": "Malicious Actors",
            "subdomain": "4.3 Cyberattacks, weapons development or use",
        },
        {
            "id": "MIT-RISK-H001",
            "title": "Overreliance on AI and unsafe use",
            "description": "Users anthropomorphizing or excessively trusting AI systems, leading to emotional dependence, exploitation by malicious actors, or harm from inappropriate use in critical situations.",
            "domain": "Human-Computer Interaction",
            "subdomain": "5.1 Overreliance and unsafe use",
        },
        {
            "id": "MIT-RISK-H002",
            "title": "Loss of human agency and autonomy to AI systems",
            "description": "Humans delegating key decisions to AI, diminishing human control and autonomy, potentially leading to disempowerment and cognitive enfeeblement.",
            "domain": "Human-Computer Interaction",
            "subdomain": "5.2 Loss of human agency and autonomy",
        },
        {
            "id": "MIT-RISK-S001",
            "title": "AI-driven power centralization and inequality",
            "description": "AI concentrating power and resources within entities that own or control advanced AI systems, leading to inequitable distribution of benefits and increased inequality.",
            "domain": "Socioeconomic & Environmental",
            "subdomain": "6.1 Power centralization",
        },
        {
            "id": "MIT-RISK-S002",
            "title": "AI-induced employment decline and economic inequality",
            "description": "Widespread AI automation reducing employment quality, creating exploitative dependencies, and increasing socioeconomic inequalities.",
            "domain": "Socioeconomic & Environmental",
            "subdomain": "6.2 Increased inequality",
        },
        {
            "id": "MIT-RISK-S003",
            "title": "AI governance failure and inadequate regulation",
            "description": "Regulatory frameworks failing to keep pace with AI development, leading to ineffective governance and inability to manage AI risks.",
            "domain": "Socioeconomic & Environmental",
            "subdomain": "6.5 Governance failure",
        },
        {
            "id": "MIT-RISK-T001",
            "title": "AI misalignment with human goals and values",
            "description": "AI systems acting in conflict with human goals or values through reward hacking, goal misgeneralisation, or dangerous capabilities like manipulation and deception.",
            "domain": "AI System Safety, Failures, & Limitations",
            "subdomain": "7.1 AI pursuing own goals",
        },
        {
            "id": "MIT-RISK-T002",
            "title": "AI lacking capability or robustness",
            "description": "AI systems failing to perform reliably under varying conditions, exposing them to errors with significant consequences in critical applications.",
            "domain": "AI System Safety, Failures, & Limitations",
            "subdomain": "7.3 Lack of capability or robustness",
        },
        {
            "id": "MIT-RISK-T003",
            "title": "Lack of transparency and interpretability in AI",
            "description": "Inability to understand or explain AI decision-making, leading to mistrust, difficulty enforcing compliance, and inability to identify and correct errors.",
            "domain": "AI System Safety, Failures, & Limitations",
            "subdomain": "7.4 Lack of transparency or interpretability",
        },
    ]

    results = []
    for entry in curated:
        domain = entry["domain"]
        sev = SEVERITY_BY_DOMAIN.get(domain, 3)
        like = LIKELIHOOD_BY_DOMAIN.get(domain, 3)
        results.append({
            "id": entry["id"],
            "title": entry["title"],
            "description": entry["description"],
            "source": "MIT AI Risk Repository",
            "classification": f"domain:{domain}/sub:{entry['subdomain']}",
            "mitre_tactic": domain,
            "severity": sev,
            "likelihood": like,
            "published_date": "2024-08-01",
            "remediation": (
                f"Aplicar controles del dominio '{domain}' según MIT AI Risk Repository. "
                f"Subdominio: {entry['subdomain']}."
            ),
            "nist_controls": [
                f"NIST AI RMF - {domain}",
                "ISO 42001:2023",
                "ISO 23894:2023",
            ],
            "affected_systems": ["AI Systems", "ML Applications", "Generative AI"],
            "url": "https://airisk.mit.edu",
        })
    return results[:limit]


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 4 (Complementaria): NVD (National Vulnerability Database) — API real
# ══════════════════════════════════════════════════════════════════════════════

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_nvd_cve(keywords: list[str] | None = None, limit: int = 10) -> list[dict]:
    """Busca CVEs reales relacionados con IA/ML en NVD."""
    if keywords is None:
        keywords = [
            "artificial intelligence", "machine learning", "ai model",
            "llm", "neural network", "tensorflow", "pytorch",
            "adversarial", "prompt injection", "generative ai",
        ]
    results = []
    for kw in keywords:
        try:
            resp = requests.get(
                NVD_API,
                params={
                    "keywordSearch": kw,
                    "resultsPerPage": min(limit, 20),
                },
                headers=HEADERS,
                timeout=HTTP_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            vulnerabilities = data.get("vulnerabilities", [])
            for item in vulnerabilities[:limit]:
                cve = item.get("cve", {})
                cve_id = cve.get("id", "N/A")
                # Evitar duplicados
                if any(r["id"] == cve_id for r in results):
                    continue
                metrics = cve.get("metrics", {})
                cvss_data = (
                    metrics.get("cvssMetricV31", [{}])[0]
                    or metrics.get("cvssMetricV30", [{}])[0]
                    or {}
                )
                cvss = cvss_data.get("cvssData", {})
                base_score = cvss.get("baseScore", 0)
                severity_nvd = max(1, min(5, int(base_score / 2))) if base_score else 3

                results.append({
                    "id": cve_id,
                    "title": (cve.get("descriptions", [{}])[0].get("value", "")[:200]),
                    "description": cve.get("descriptions", [{}])[0].get("value", ""),
                    "source": "NVD",
                    "classification": f"CVE-{severity_nvd}",
                    "mitre_tactic": f"CVE (CVSS: {base_score})",
                    "severity": severity_nvd,
                    "likelihood": max(1, min(5, severity_nvd - 1)),
                    "published_date": cve.get("published", ""),
                    "remediation": (
                        f"Aplicar parche del vendor. "
                        f"CVSS v3: {base_score}/10 ({cvss.get('baseSeverity', 'N/A')}). "
                        f"Consultar https://nvd.nist.gov/vuln/detail/{cve_id}"
                    ),
                    "nist_controls": [
                        "NIST SP 800-53 RA-5 - Scanning de vulnerabilidades",
                        "ISO 27001:2022 A.8.8 - Gestión de vulnerabilidades técnicas",
                    ],
                    "affected_systems": keywords[:3],
                    "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                })
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"[NVD] Error para keyword '{kw}': {e}")
            continue
    return results[:limit]


# ══════════════════════════════════════════════════════════════════════════════
# FUENTE 5: AI Incident Database (incidentdatabase.ai)
# RSS Feed: https://incidentdatabase.ai/rss.xml (público, sin autenticación)
# Backups semanales: https://incidentdatabase.ai/research/snapshots/ (CSV/JSON)
# ══════════════════════════════════════════════════════════════════════════════

AIID_RSS_URL = "https://incidentdatabase.ai/rss.xml"
AIID_BACKUP_URL = "https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/backup-20260525112454.tar.bz2"


def fetch_aiid_incidents(limit: int = 10) -> list[dict]:
    """
    Consulta la AI Incident Database vía RSS Feed público.
    Contiene incidentes reales de IA documentados desde 2014.
    Más de 1500 incidentes catalogados por el Responsible AI Collaborative.
    """
    import xml.etree.ElementTree as ET

    try:
        resp = requests.get(AIID_RSS_URL, headers=HEADERS, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        items = root.findall(".//item")
        results = []

        for item in items[:limit]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")
            pub_date = item.findtext("pubDate", "")
            guid = item.findtext("guid", "")

            # Extraer incident_id del GUID o link
            import re
            incident_match = re.search(r"/cite/(\d+)", link or guid or "")
            incident_id = incident_match.group(1) if incident_match else "0"
            report_num = guid.split("-")[-1] if guid else "0"

            clasificacion = "Tecnico"
            t_lower = (title + " " + (desc or "")).lower()
            if any(w in t_lower for w in ["bias", "fairness", "discriminat", "gender", "racial"]):
                clasificacion = "Sesgo"
            elif any(w in t_lower for w in ["privacy", "leak", "data breach", "expos"]):
                clasificacion = "Privacidad"
            elif any(w in t_lower for w in ["deepfake", "misinform", "disinform", "fake"]):
                clasificacion = "Societal"
            elif any(w in t_lower for w in ["injection", "jailbreak", "adversar", "evasion"]):
                clasificacion = "Adversarial"
            elif any(w in t_lower for w in ["crash", "accident", "safety", "death", "injure", "robot"]):
                clasificacion = "Seguridad Fisica"

            results.append({
                "id": f"AIID-{incident_id}",
                "title": title[:200],
                "description": (desc or title)[:500],
                "source": "AI Incident Database",
                "classification": clasificacion,
                "mitre_tactic": f"AIID/{clasificacion}",
                "severity": 3,
                "likelihood": 3,
                "published_date": pub_date[:10] if pub_date else "",
                "remediation": (
                    f"Incidente documentado en la AI Incident Database. "
                    f"Ver {link} para detalles completos."
                ),
                "nist_controls": [
                    "NIST AI RMF - Incident Response",
                    "ISO 42001:2023 A.7 - Seguridad en IA",
                ],
                "affected_systems": ["AI Systems"],
                "url": link,
            })
        return results

    except Exception as e:
        print(f"[AIID RSS] Error: {e}. Intentando backup semanal...")
        return _fetch_aiid_backup(limit)


def _fetch_aiid_backup(limit: int) -> list[dict]:
    """
    Fallback: descarga el backup semanal más reciente.
    El archivo es un tar.bz2 con JSON completo de ~97MB.
    """
    try:
        import tarfile
        import io

        resp = requests.get(AIID_BACKUP_URL, headers=HEADERS, timeout=120)
        resp.raise_for_status()

        results = []
        with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:bz2") as tar:
            for member in tar.getmembers():
                if member.name.endswith(".json") and "incidents" in member.name.lower():
                    f = tar.extractfile(member)
                    if f:
                        data = json.loads(f.read())
                        incidents = data if isinstance(data, list) else data.get("incidents", data.get("data", []))
                        for inc in incidents[:limit]:
                            title = inc.get("title", inc.get("name", ""))[:200]
                            desc = inc.get("description", inc.get("report", ""))[:500]
                            incident_id = inc.get("incident_id", inc.get("id", "0"))
                            results.append({
                                "id": f"AIID-BK-{incident_id}",
                                "title": title,
                                "description": desc,
                                "source": "AI Incident Database (backup)",
                                "classification": "Tecnico",
                                "mitre_tactic": "AIID/backup",
                                "severity": 3,
                                "likelihood": 3,
                                "published_date": inc.get("date", ""),
                                "remediation": "Ver AI Incident Database para detalles del incidente.",
                                "nist_controls": ["NIST AI RMF - Incident Response"],
                                "affected_systems": ["AI Systems"],
                                "url": f"https://incidentdatabase.ai/cite/{incident_id}",
                            })
                        break
        return results[:limit]

    except Exception as e:
        print(f"[AIID Backup] Error: {e}")
        return []


# ══════════════════════════════════════════════════════════════════════════════
# ORQUESTADOR
# ══════════════════════════════════════════════════════════════════════════════

def fetch_all(limit_per_source: int = 5, include_nvd: bool = False, include_aiid: bool = False) -> list[dict]:
    """
    Obtiene vulnerabilidades reales de todas las fuentes disponibles.
    MITRE ATLAS → YAML oficial del repositorio GitHub
    AVID → JSON individuales del repositorio GitHub
    MIT AI Risk → Taxonomía curada del MIT
    NVD → API del gobierno de EEUU (opcional)
    AI Incident Database → GraphQL pública (opcional)
    """
    results = []
    errors = []

    # 1. MITRE ATLAS
    try:
        atlas = fetch_mitre_atlas(limit=limit_per_source)
        results.extend(atlas)
        print(f"[MITRE ATLAS] {len(atlas)} técnicas obtenidas")
    except Exception as e:
        errors.append(f"MITRE ATLAS: {e}")

    # 2. AVID
    try:
        avid = fetch_avid_reports(limit=limit_per_source)
        results.extend(avid)
        print(f"[AVID] {len(avid)} vulnerabilidades obtenidas")
    except Exception as e:
        errors.append(f"AVID: {e}")

    # 3. MIT AI Risk Repository
    try:
        mit = fetch_mit_risk_repo(limit=limit_per_source)
        results.extend(mit)
        print(f"[MIT AI Risk] {len(mit)} riesgos obtenidos")
    except Exception as e:
        errors.append(f"MIT AI Risk: {e}")

    # 4. NVD (opcional)
    if include_nvd:
        try:
            nvd = fetch_nvd_cve(limit=limit_per_source)
            results.extend(nvd)
            print(f"[NVD] {len(nvd)} CVEs obtenidos")
        except Exception as e:
            errors.append(f"NVD: {e}")

    # 5. AI Incident Database (opcional)
    if include_aiid:
        try:
            aiid = fetch_aiid_incidents(limit=limit_per_source)
            results.extend(aiid)
            print(f"[AIID] {len(aiid)} incidentes obtenidos")
        except Exception as e:
            errors.append(f"AIID: {e}")

    for err in errors:
        print(f"[WARN] {err}")

    return results
