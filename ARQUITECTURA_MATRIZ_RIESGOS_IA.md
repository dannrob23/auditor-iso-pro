# Módulo Matriz de Riesgos de IA

## Arquitectura y Funcionamiento

---

## 1. Propósito

Módulo de ingesta, normalización, clasificación y exportación de vulnerabilidades de Inteligencia Artificial. Construye una base de conocimiento curada y actualizada automáticamente para alimentar la Matriz de Riesgos de IA del Framework IA-SEC (ISO 27001 + NIST AI RMF + ISO 42001).

---

## 2. Estructura del Módulo

```
ingestor/
├── __init__.py          # Export público
├── sources.py           # 5 fuentes de vulnerabilidades reales
├── normalizer.py        # Normalización y traducción a español
├── risk_matrix.py       # Cálculo de riesgo (matriz 5x5), clasificación
├── context_prompt.py    # Cuestionario contextual de la organización
└── excel_export.py      # Exportación a Excel profesional

database.py              # SQLite (almacenamiento persistente)
data/
├── reportes.db          # Base de datos SQLite
└── Matriz_Riesgos_IA.xlsx  # Excel de respaldo (generado automáticamente)
```

---

## 3. Fuentes de Datos

| Fuente | Método de Consulta | Contenido |
|---|---|---|
| **MITRE ATLAS** | `requests.get()` al YAML oficial en `raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml` | 101 técnicas adversariales contra sistemas de IA, organizadas en 14 tácticas (Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Defense Evasion, Discovery, Collection, Exfiltration, Impact, etc.) |
| **AVID** (AI Vulnerability Database) | `requests.get()` a `raw.githubusercontent.com/avidml/avid-db/main/vulnerabilities/{año}/{id}.json` | 33 vulnerabilidades documentadas con casos reales: sesgo algorítmico, ataques adversariales, fallos de seguridad física, problemas de privacidad |
| **MIT AI Risk Repository** | Taxonomía curada del paper arXiv:2408.12622 del MIT | 18 riesgos categorizados en 7 dominios: Discriminación & Toxicidad, Privacidad & Seguridad, Desinformación, Actores Maliciosos, Interacción Humano-Computador, Riesgos Socioeconómicos, Seguridad y Fallos del Sistema |
| **AI Incident Database** (incidentdatabase.ai) | RSS Feed público (`/rss.xml`) | Incidentes reales de IA documentados desde 2014 por el Responsible AI Collaborative |
| **NVD** (National Vulnerability Database) | API REST del gobierno de EE.UU. (`services.nvd.nist.gov`) — opcional | CVEs de IA en bibliotecas como TensorFlow, PyTorch, LangChain |

Cada fuente tiene una función dedicada (`fetch_mitre_atlas()`, `fetch_avid_reports()`, `fetch_mit_risk_repo()`, `fetch_aiid_incidents()`, `fetch_nvd_cve()`) con manejo de errores HTTP, timeouts de 30s y headers estándar.

---

## 4. Normalización

Cada vulnerabilidad se normaliza a un esquema unificado de 22 campos. El proceso puede usar:

### 4.1 DeepSeek (modo IA, recomendado)
Si `DEEPSEEK_API_KEY` está configurada en `.env`, cada vulnerabilidad se envía al modelo `deepseek-chat` con un system prompt que pide:
- Traducción completa a español con lenguaje sencillo
- Clasificación por tipo (Adversarial, Privacidad, Sesgo, Seguridad Física, Datos, Societal, Técnico)
- Explicación de causa raíz, cómo se ejecuta el ataque y cómo prevenirlo
- Asignación de probabilidad (1-5), severidad (1-5) y normas aplicables
- Asignación de normativa colombiana según el tipo

### 4.2 Normalizador local (modo offline)
Si DeepSeek no está disponible, el sistema usa reglas lingüísticas y mapeo de palabras clave para:
- Clasificar por tipo (según palabras en el título o descripción)
- Generar explicaciones en español predefinidas para cada tipo
- Asignar probabilidad, severidad y normas aplicables
- Asignar normativa colombiana según el tipo

### Campos normalizados

| Campo | Descripción | Ejemplo |
|---|---|---|
| `id_vulnerabilidad` | ID único de la fuente | `AVID-2022-V001` |
| `fuente_origen` | Fuente de procedencia | `MITRE ATLAS` |
| `resumen_es` | Resumen en español | "El modelo BERT muestra sesgo de género..." |
| `descripcion_riesgo` | Impacto al negocio | "El sistema discrimina a ciertos grupos..." |
| `causa_raiz` | Causa técnica explicada simple | "Los datos de entrenamiento contenían sesgos..." |
| `accion_remediacion` | Solución recomendada | "Auditar los datos, usar conjuntos balanceados..." |
| `como_se_ejecuta` | Cómo ejecuta el ataque | "El atacante envía datos modificados..." |
| `como_prevenirlo` | Medidas prácticas para evitarlo | "Validar entradas, supervisión humana..." |
| `tactica_mitre` | Táctica MITRE ATLAS | `AML.T0051 - Prompt Injection` |
| `clasificacion_tipo` | Tipo de vulnerabilidad | `Sesgo`, `Adversarial`, `Privacidad` |
| `probabilidad_base` | Probabilidad (1-5) | `4` |
| `severidad_tecnica` | Severidad (1-5) | `4` |
| `normas_aplicables` | Lista de normas que mitigan | `["NIST AI RMF 2.6", "ISO 42001 A.6.2"]` |
| `normativa_colombia` | Normativa colombiana aplicable | `["Ley 1581/2012", "CONPES 4069/2022"]` |
| `controles_nist` | Control NIST recomendado | `NIST AI RMF 3.0 Robustness Testing` |
| `sistemas_afectados` | Sistemas impactados | `["Healthcare LLM", "Clinical Systems"]` |

---

## 5. Cálculo del Riesgo (Matriz 5×5)

Se utiliza la metodología de la **matriz cualitativa de riesgo 5×5** basada en ISO 31000:2018 e ISO 27005:2022:

```
Riesgo = Probabilidad × Severidad
```

| Probabilidad \ Severidad | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | 5 | 10 | 15 | 20 | **25** |
| **4** | 4 | 8 | 12 | **16** | **20** |
| **3** | 3 | 6 | **9** | **12** | **15** |
| **2** | 2 | **4** | **6** | **8** | **10** |
| **1** | **1** | **2** | **3** | **4** | **5** |

### Niveles de Riesgo

| Rango | Nivel | Acción Requerida |
|---|---|---|
| 1-5 | **BAJO** | Riesgo aceptable. Controles existentes suficientes. |
| 6-11 | **MEDIO** | Riesgo tolerable. Monitoreo y mejora planificada. |
| 12-19 | **ALTO** | Riesgo inaceptable. Acciones correctivas inmediatas. |
| 20-25 | **EXTREMO** | Riesgo crítico. Escalamiento a dirección. |

### Criticidad Compuesta

Adicionalmente se calcula un índice de criticidad en escala 0-100:

```
Criticidad = ((Probabilidad + Severidad) / 10) × 100
```

---

## 6. Clasificación de Vulnerabilidades

Cada vulnerabilidad se clasifica en una de siete categorías según su naturaleza:

| Categoría | Significado | Ejemplo |
|---|---|---|
| **Adversarial** | Un atacante manipula el sistema para que dé respuestas incorrectas | Prompt injection, evasión de modelos, adversarial patches |
| **Sesgo** | El sistema discrimina a ciertos grupos de personas | Sesgo de género en modelos de lenguaje, discriminación racial en crédito |
| **Privacidad** | El sistema expone información privada | Model inversion, membership inference, fuga de datos de entrenamiento |
| **Seguridad Física** | El sistema puede causar daños físicos | Vehículo autónomo que atropella, robot que lastima trabajadores |
| **Datos** | Los datos del sistema están contaminados | Data poisoning, backdoor en datos de entrenamiento, supply chain |
| **Societal** | El sistema afecta negativamente a la sociedad | Deepfakes, desinformación masiva, vigilancia sin consentimiento |
| **Técnico** | El sistema tiene debilidades de infraestructura | APIs sin autenticación, configuraciones inseguras |

La clasificación se asigna automáticamente según:
1. La táctica MITRE ATLAS asociada
2. Palabras clave en el título y descripción de la vulnerabilidad
3. El dominio del MIT AI Risk Repository
4. El contenido del título en AVID

---

## 7. Normativa Colombiana Aplicable

Cada vulnerabilidad recibe 4 normas colombianas específicas según su tipo:

| Tipo | Normas Colombianas |
|---|---|
| **Adversarial** | Ley 1581/2012 (principio de seguridad), Circular 007/2018 SFC, CONPES 3995/2020, Resolución MinTIC 2022 |
| **Privacidad** | Ley 1581/2012 (Art. 4,10,17), Decreto 1377/2013, Ley 1266/2008 (Habeas Data), CONPES 4069/2022 |
| **Sesgo** | Ley 1581/2012 Art. 4 (no discriminación), CONPES 4069/2022 Eje 2, Proyecto Ley 059/2023, Decreto 1081/2015 |
| **Seguridad Física** | CONPES 3995/2020 (infraestructura crítica), Resolución MinTIC 2022, Ley 2195/2022, CONPES 4069/2022 |
| **Datos** | Ley 1581/2012, Decreto 1377/2013 Art. 11, Decreto 1074/2015, CONPES 4069/2022 |
| **Societal** | CONPES 4069/2022, Proyecto Ley 059/2023, Ley 2195/2022, Ley 1712/2014 |
| **Técnico** | Resolución MinTIC 2022, CONPES 3995/2020, Decreto 620/2020, NTC-ISO 27001 |

---

## 8. Persistencia

Los datos se almacenan en **SQLite** (archivo `data/reportes.db`) en la tabla `vulnerabilidades_ia` con 24 columnas, índices por fuente y nivel de riesgo, y deduplicación por `id_vulnerabilidad` (clave UNIQUE).

La función `exportar_excel_respaldo()` genera automáticamente un Excel en `data/Matriz_Riesgos_IA.xlsx` cada vez que se actualiza el feed.

---

## 9. Actualización Automática

El módulo se integra con la aplicación Streamlit (`app.py`) y:

1. **Al cargar el tab "Matriz Riesgos IA"**: Verifica si pasó más de 1 hora desde la última actualización. Si es así, consulta todas las fuentes, normaliza, guarda y genera el Excel automáticamente.

2. **Botón "Actualizar ahora"**: Fuerza una actualización inmediata con barra de progreso, mostrando cuántas vulnerabilidades nuevas se insertaron y cuántas antiguas se desactivaron.

3. **Selector de intervalo**: Permite elegir entre Manual, 1h, 6h, 12h, 24h para las actualizaciones automáticas.

4. **Limpieza automática**: Vulnerabilidades con más de 90 días se desactivan (no se borran, solo se marcan como inactivas).

---

## 10. Cuestionario Contextual

Antes de generar la matriz, un cuestionario de 11 preguntas captura el contexto de la organización:

1. **País** — Colombia, Latinoamérica, EE.UU., Europa, Otro
2. **Sector** — Energía, Salud, Finanzas, Transporte, Gobierno, Telecomunicaciones, Agua, Tecnología, Educación
3. **Tamaño** — Pequeña, Mediana, Grande, Corporación
4. **Sistemas de IA** — Chatbots, Visión por computadora, Modelos predictivos, NLP, Robótica, etc.
5. **Normas aplicables** — ISO 27001, ISO 42001, NIST AI RMF, PCI DSS, HIPAA, etc.
6. **Exposición** — APIs públicas, redes internas, sistemas aislados
7. **Incidentes previos** — Historial de incidentes de IA en los últimos 12 meses
8. **Madurez de gobierno IA** — Inexistente, Inicial, Definido, Gestionado, Optimizado
9. **Datos sensibles** — Personales, biométricos, financieros, infraestructura crítica
10. **Proveedores de IA** — Comerciales, open source, propios
11. **Objetivo** — Cumplimiento regulatorio, gestión de riesgos, preparación para auditoría

---

## 11. Exportación a Excel

El Excel generado contiene **6 pestañas** en español:

| Pestaña | Contenido |
|---|---|
| **Tablero de Control** | Métricas generales (total, extremos, altos, medios, bajos), distribución por fuente y tipo |
| **Metodología** | Explicación completa del marco normativo, fuentes, clasificaciones, cálculo del riesgo, normativa colombiana |
| **Catálogo de Vulnerabilidades** | Lista completa con ID, fuente, descripción, causa raíz, cómo se ejecuta, cómo prevenirlo, solución, clasificación, táctica MITRE, probabilidad, severidad, nivel de riesgo, normas aplicables, normativa colombiana |
| **Clasificación por Táctica** | Vulnerabilidades agrupadas por código de táctica MITRE con descripción, cantidad, riesgo promedio y porcentaje |
| **Mapa de Calor P×S** | Matriz visual 5×5 con colores (rojo=EXTREMO, naranja=ALTO, amarillo=MEDIO, verde=BAJO) más leyenda |
| **Controles y Normas Aplicables** | Cada vulnerabilidad con control recomendado, normas aplicables, tipo, prioridad, nivel de riesgo, normativa colombiana |

---

## 12. Diagrama de Flujo

```
[Fuentes]                    [Normalización]          [Cálculo]              [Salida]
                                                                               
MITRE ATLAS (YAML)        ┐                                                 ┌► SQLite
AVID (JSON)               ├──► DeepSeek/Local     ──► Matriz 5×5         ──┼► Excel 6 pestañas
MIT AI Risk (taxonomía)   │    Traducción a ES        Riesgo = P × S       ├► UI Streamlit
AI Incident DB (RSS)      │    Clasificación          Criticidad 0-100     └► Sidebar descarga
NVD (API, opcional)       ┘    Normas aplicables                           
                               Normativa Colombia                          
                                        │                                    
                                        ▼                                    
                              [Cuestionario contextual]                      
                              11 preguntas → prompt personalizado           
```

---

## 13. Tecnologías Utilizadas

- **Python 3.14+**
- **Streamlit** — Interfaz de usuario
- **SQLite** — Base de datos (sin servidor, archivo único)
- **DeepSeek API** — Traducción y normalización con IA
- **openpyxl** — Generación de archivos Excel
- **requests** — Consultas HTTP a fuentes externas
- **PyYAML** — Parseo del YAML de MITRE ATLAS
- **Plotly** — Gráficos interactivos en la UI
- **pandas** — Manejo de datos tabulares

---

## 14. Citas y Referencias

- MITRE ATLAS: https://atlas.mitre.org
- AVID (AI Vulnerability Database): https://avidml.org
- MIT AI Risk Repository: https://airisk.mit.edu — arXiv:2408.12622
- AI Incident Database: https://incidentdatabase.ai — arXiv:2011.08512
- NVD: https://nvd.nist.gov
- ISO 31000:2018 — Gestión del riesgo
- ISO 27005:2022 — Gestión de riesgos de seguridad de la información
- NIST AI RMF 1.0 — AI Risk Management Framework
- ISO 42001:2023 — Sistema de Gestión de IA
- CONPES 3995/2020 — Política Nacional de Ciberseguridad (Colombia)
- CONPES 4069/2022 — Política Nacional de Inteligencia Artificial (Colombia)
- Ley 1581/2012 — Protección de Datos Personales (Colombia)
