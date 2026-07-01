# IA-SEC Auditor Tool

## Tutorial Completo de la Herramienta de Auditoría de Inteligencia Artificial

**Versión:** 1.0  
**Propósito:** Framework de Auditoría de IA basado en ISO 27001, ISO 42001, NIST AI RMF, ISO 19011 e ISO 23894  
**Público objetivo:** Empresas, auditores, profesores y estudiantes de ciberseguridad e inteligencia artificial

---

## Tabla de Contenido

1. [¿Qué es IA-SEC Auditor Tool?](#1-qué-es-ia-sec-auditor-tool)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación y Primeros Pasos](#3-instalación-y-primeros-pasos)
4. [Módulo 1: Chat Auditor](#4-módulo-1-chat-auditor)
5. [Módulo 2: Auditoría de IA (Gap Analysis)](#5-módulo-2-auditoría-de-ia-gap-analysis)
6. [Módulo 3: Texto Libre](#6-módulo-3-texto-libre)
7. [Módulo 4: Base RAG (NotebookLM)](#7-módulo-4-base-rag-notebooklm)
8. [Módulo 5: Confluencia](#8-módulo-5-confluencia)
9. [Módulo 6: Interoperabilidad](#9-módulo-6-interoperabilidad)
10. [Módulo 7: Matriz de Riesgos IA](#10-módulo-7-matriz-de-riesgos-ia)
11. [Módulo 8: Autodiagnóstico](#11-módulo-8-autodiagnóstico)
12. [Módulo 9: Dashboard](#12-módulo-9-dashboard)
13. [Módulo 10: Historial](#13-módulo-10-historial)
14. [Módulo 11: Guía del Auditor](#14-módulo-11-guía-del-auditor)
15. [Módulo 12: Rol del Auditor](#15-módulo-12-rol-del-auditor)
16. [Módulo 13: Logs de Auditoría](#16-módulo-13-logs-de-auditoría)
17. [Base de Conocimiento de Vulnerabilidades IA](#17-base-de-conocimiento-de-vulnerabilidades-ia)
18. [Exportación de Resultados](#18-exportación-de-resultados)
19. [Preguntas Frecuentes](#19-preguntas-frecuentes)

---

## 1. ¿Qué es IA-SEC Auditor Tool?

IA-SEC Auditor Tool es una plataforma integral de auditoría de sistemas de Inteligencia Artificial diseñada para:

- **Empresas**: Evaluar el cumplimiento normativo de sus sistemas de IA frente a estándares internacionales (ISO 27001, ISO 42001, NIST AI RMF), generando reportes de brechas (Gap Analysis) accionables.
- **Auditores**: Automatizar el proceso de auditoría de IA, desde la ingesta de políticas hasta la generación de matrices de riesgos y planes de tratamiento.
- **Profesores y estudiantes**: Enseñar y aprender sobre los marcos normativos de IA, la identificación de vulnerabilidades en sistemas de IA, y la elaboración de matrices de riesgo.

### Normas y Estándares Soportados

| Norma | Enfoque | Uso en la Herramienta |
|---|---|---|
| **ISO/IEC 27001:2022** | Seguridad de la Información | Controles base — Gestión de vulnerabilidades (A.8.8), Control de acceso (A.8), Protección de datos (A.8.12) |
| **ISO/IEC 42001:2023** | Sistema de Gestión de IA | Controles específicos para IA — A.7 Seguridad, A.6 Explicabilidad y equidad |
| **NIST AI RMF 1.0** | Gestión de Riesgos de IA | Funciones GOVERN, MAP, MEASURE, MANAGE — Taxonomía de riesgos técnicos de IA |
| **ISO/IEC 23894:2023** | Gestión de Riesgos de IA | Guía para la gestión de riesgos específicos de IA |
| **ISO 19011:2018** | Auditoría de Sistemas de Gestión | Principios y guía para la realización de auditorías |

### Funcionalidades Principales

- **Gap Analysis**: Compara políticas de seguridad de IA contra ISO 27001, ISO 42001 y NIST AI RMF, identificando brechas y generando planes de acción.
- **Matriz de Riesgos IA**: Consulta automática de 4 fuentes especializadas (MITRE ATLAS, AVID, MIT AI Risk Repository, AI Incident Database) para mantener una base de conocimiento actualizada de vulnerabilidades de IA.
- **RAG (Retrieval-Augmented Generation)**: Base de conocimiento que permite buscar en documentos normativos cargados.
- **Interoperabilidad**: Evaluación de conformidad con el Marco de Interoperabilidad del Estado colombiano.
- **Autodiagnóstico**: Encuesta de madurez en gobierno de IA.
- **Exportación**: Reportes en Excel profesional, PDF y Markdown.

---

## 2. Requisitos del Sistema

### Hardware
- **Procesador**: Intel Core i5 o superior (o equivalente)
- **RAM**: 8 GB mínimo (16 GB recomendado)
- **Disco**: 2 GB de espacio libre
- **Conexión a Internet**: Requerida para consultar fuentes de vulnerabilidades y usar modelos de IA

### Software
- **Sistema Operativo**: Linux (recomendado), Windows o macOS
- **Python**: 3.10 o superior
- **Navegador**: Chrome, Firefox, Edge o Safari (actualizado)

### Dependencias
Las dependencias se instalan automáticamente con el archivo `requirements.txt` incluido en el proyecto.

---

## 3. Instalación y Primeros Pasos

### 3.1 Clonar o Descargar el Proyecto

```bash
git clone https://github.com/tu-repositorio/ia-sec-auditor.git
cd ia-sec-auditor
```

### 3.2 Crear Entorno Virtual e Instalar Dependencias

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
pip install -r requirements.txt
```

### 3.3 Configurar Variables de Entorno

Copia el archivo de ejemplo y configura las APIs:

```bash
cp .env.example .env
```

Edita `.env` con tus claves:

```
DEEPSEEK_API_KEY=sk-tu-api-key-deepseek
GOOGLE_API_KEY=tu-api-key-de-gemini
```

> **Nota**: La herramienta funciona sin API keys usando el normalizador local. DeepSeek solo se requiere para la traducción avanzada de vulnerabilidades.

### 3.4 Iniciar la Aplicación

```bash
streamlit run app.py --server.port 8501
```

Abre en el navegador: `http://localhost:8501`

### 3.5 Iniciar Sesión

| Campo | Valor |
|---|---|
| **Usuario** | `auditor` |
| **Contraseña** | `Auditor2024!` |

> Estas credenciales se pueden cambiar en el archivo `config.yaml`.

---

## 4. Módulo 1: Chat Auditor

### Propósito
Asistente conversacional impulsado por IA que responde preguntas sobre normativas de IA, ciberseguridad y auditoría.

### ¿Cómo funciona?
1. Selecciona el proveedor de IA en el panel lateral (DeepSeek, Google Gemini u OpenAI).
2. Escribe tu pregunta en el campo de texto al final de la pantalla.
3. El asistente responde basado en el contexto de las normativas configuradas.

### Ejemplos de preguntas
- "¿Qué controles del Anexo A de ISO 27001 aplican a sistemas de IA?"
- "Explica la diferencia entre ISO 42001 y NIST AI RMF"
- "¿Cómo auditar un sistema de recomendación basado en IA?"
- "¿Qué dice la Ley 1581 de 2012 sobre protección de datos en IA?"

### Caso de uso
Un estudiante que está aprendiendo sobre ISO 42001 puede preguntar directamente al asistente y obtener respuestas contextualizadas con la normativa.

---

## 5. Módulo 2: Auditoría de IA (Gap Analysis)

### Propósito
Motor principal de auditoría. Analiza documentos PDF de políticas de seguridad de IA y los compara contra los controles de ISO 27001, ISO 42001 y NIST AI RMF.

### ¿Cómo funciona?
1. **Subir documento**: Arrastra o selecciona un archivo PDF que contenga la política de seguridad de IA de la organización.
2. **Ejecutar Gap Analysis**: Haz clic en "🔍 Ejecutar Gap Analysis".
3. **Resultado**: La herramienta analiza el documento y genera:
   - **Controles conformes**: Los que la política cubre adecuadamente.
   - **Controles parciales**: Los que cubre pero con deficiencias.
   - **No conformidades**: Controles no cubiertos en absoluto.
   - **Porcentaje de cumplimiento**: Métrica global de adherencia.

### Formato de Salida
- **Resumen ejecutivo**: Tablero con métricas y semáforos.
- **Detalle de hallazgos**: Cada control analizado con su estado y recomendaciones.
- **Plan de acción**: Recomendaciones priorizadas para cerrar las brechas identificadas.
- **Exportar**: PDF, Markdown o TXT.

### Caso de uso
Un auditor recibe la política de seguridad de IA de un banco. Sube el PDF, ejecuta el análisis y obtiene un reporte de 45 controles evaluados con un 67% de cumplimiento y recomendaciones específicas para cada brecha.

---

## 6. Módulo 3: Texto Libre

### Propósito
Permite pegar texto directamente (políticas, procedimientos, normativas internas) sin necesidad de un archivo PDF, y ejecutar el mismo Gap Analysis.

### ¿Cómo funciona?
1. Pega el texto en el área de texto.
2. Haz clic en "🔍 Analizar Texto".
3. Obtienes el mismo análisis detallado que en el Módulo 2.

### Diferencia con el Módulo 2
| Característica | Módulo 2 (PDF) | Módulo 3 (Texto Libre) |
|---|---|---|
| Entrada | Archivo PDF | Texto pegado directamente |
| Límite de tamaño | 200MB | 50,000 caracteres |
| Ideal para | Documentos formales | Notas, borradores, políticas cortas |

---

## 7. Módulo 4: Base RAG (NotebookLM)

### Propósito
Sistema de Recuperación Aumentada por Generación (RAG) que permite cargar documentos normativos y hacer preguntas sobre su contenido.

### ¿Cómo funciona?
1. **Cargar documentos**: Sube archivos PDF, TXT o Markdown al repositorio de conocimiento.
2. **Indexar**: La herramienta procesa y vectoriza el contenido usando FAISS (Facebook AI Similarity Search).
3. **Consultar**: Escribe preguntas sobre los documentos cargados y el sistema responde citando las fuentes relevantes.

### ¿Qué documentos cargar?
- ISO 27001:2022 (completo)
- ISO 42001:2023
- NIST AI RMF 1.0
- Ley 1581 de 2012 (Colombia)
- CONPES 4069 de 2022
- Políticas internas de la organización

### Caso de uso
Un profesor carga los 7 dominios del MIT AI Risk Repository y pide: "¿Qué riesgos del dominio de privacidad aplican a sistemas de salud?" El sistema responde citando los artículos específicos del repositorio.

---

## 8. Módulo 5: Confluencia

### Propósito
Integración con Atlassian Confluence para extraer documentación directamente desde espacios y páginas de la intranet corporativa.

### ¿Cómo funciona?
1. Configura la URL de Confluence y las credenciales en el panel lateral.
2. Selecciona el espacio de Confluence a auditar.
3. La herramienta extrae las páginas y ejecuta el Gap Analysis sobre el contenido.

### Requisitos
- Acceso a una instancia de Confluence (Cloud o Server).
- Token de API o credenciales de usuario.

---

## 9. Módulo 6: Interoperabilidad

### Propósito
Evalúa el cumplimiento del sistema de IA con el **Marco de Interoperabilidad del Estado colombiano**, basado en los 23 controles definidos para Sistemas de Información Críticos (IC).

### ¿Cómo funciona?
1. Selecciona el sector de infraestructura crítica (Salud, Energía, Finanzas, Gobierno, etc.).
2. La herramienta muestra las dimensiones y controles aplicables.
3. Marca el nivel de implementación de cada control (Implementado, Parcial, No implementado, No aplica).
4. Obtén:
   - **Porcentaje de interoperabilidad** por dimensión y global.
   - **Matriz de calor** visual.
   - **Propuesta de plan de interoperabilidad** generada por IA.
   - **Exportación a Excel** con 5 pestañas profesionales.

### Dimensiones Evaluadas
| Dimensión | Controles | Descripción |
|---|---|---|
| Gobernanza de IA | 5 | Políticas, roles, responsabilidades |
| Arquitectura | 4 | Diseño del sistema, APIs, estándares |
| Datos | 4 | Calidad, procedencia, intercambio |
| Seguridad | 5 | Autenticación, cifrado, auditoría |
| Interoperabilidad | 5 | Estándares, formatos, protocolos |

### Caso de uso
Una entidad de salud en Colombia necesita certificar que su sistema de IA de diagnóstico por imágenes cumple con el marco de interoperabilidad. Usa este módulo para autoevaluar los 23 controles y genera el reporte para la auditoría.

---

## 10. Módulo 7: Matriz de Riesgos IA

### Propósito
**El módulo estrella**. Motor de ingesta automática de vulnerabilidades de IA desde fuentes especializadas. Construye una base de conocimiento curada que alimenta la Matriz de Riesgos de IA.

### Fuentes de Datos Reales

| Fuente | Método de Consulta | Contenido |
|---|---|---|
| **MITRE ATLAS** | YAML oficial del repositorio GitHub | 101 técnicas adversariales contra sistemas de IA |
| **AVID** | JSON del repositorio GitHub oficial | 33 vulnerabilidades documentadas con casos reales |
| **MIT AI Risk Repository** | Taxonomía curada del MIT (arXiv:2408.12622) | 18 categorías de riesgo en 7 dominios |
| **AI Incident Database** | RSS Feed público (incidentdatabase.ai) | Incidentes reales de IA desde 2014 |
| **NVD** (opcional) | API REST del gobierno de EE.UU. | CVEs de IA en TensorFlow, PyTorch, etc. |

### Flujo de Trabajo

#### Paso 1: Cuestionario Contextual
Responde 11 preguntas sobre la organización:
1. **País** (Colombia, Latinoamérica, EE.UU., Europa, Otro)
2. **Sector** (Energía, Salud, Finanzas, Gobierno, etc.)
3. **Tamaño** (Pequeña, Mediana, Grande, Corporación)
4. **Sistemas de IA** (Chatbots, Visión, Predictivos, Robótica, etc.)
5. **Normas aplicables** (ISO 27001, ISO 42001, PCI DSS, etc.)
6. **Exposición** (APIs públicas, redes internas)
7. **Incidentes previos** (Historial de seguridad)
8. **Madurez de gobierno IA**
9. **Datos sensibles** (Personales, biométricos, financieros)
10. **Proveedores de IA** (Comerciales, open source, propios)
11. **Objetivo** (Cumplimiento, gestión de riesgos, auditoría)

#### Paso 2: Consultar Fuentes
Haz clic en "Consultar y Normalizar Fuentes". La herramienta:
1. Descarga datos de MITRE ATLAS, AVID, MIT AI Risk y AIID.
2. Normaliza cada vulnerabilidad: traduce a español, clasifica por tipo, asigna probabilidad y severidad, mapea normas aplicables.
3. Calcula el riesgo usando la **Matriz 5×5** (Probabilidad × Severidad).
4. Guarda en la base de datos SQLite sin duplicar.
5. Genera el Excel de respaldo automáticamente.

#### Paso 3: Visualizar y Exportar
- **Métricas**: Total, Extremos, Altos, Medios, Bajos, Criticidad promedio.
- **Tabla** con colores por nivel de riesgo (rojo=EXTREMO, verde=BAJO).
- **Gráficos**: Distribución por nivel y por clasificación.
- **Detalle expandible**: Cada vulnerabilidad con ID, fuente, resumen en español, causa raíz, cómo se ejecuta el ataque, cómo prevenirlo, táctica MITRE, probabilidad, severidad, nivel de riesgo, normas aplicables, normativa colombiana.
- **Exportar Excel de 6 pestañas** (ver sección 18).

### Clasificación de Vulnerabilidades

| Tipo | Descripción | Ejemplo |
|---|---|---|
| **Adversarial** | Ataques que manipulan el sistema de IA | Prompt injection, evasión de modelos, adversarial patches |
| **Sesgo** | Discriminación algorítmica | Sesgo de género en modelos de lenguaje, discriminación racial en crédito |
| **Privacidad** | Exposición de información privada | Model inversion, membership inference, fuga de datos |
| **Seguridad Física** | Daños físicos a personas o infraestructura | Vehículo autónomo que atropella, robot que lastima trabajadores |
| **Datos** | Contaminación o robo de datos de entrenamiento | Data poisoning, backdoor en datos, supply chain |
| **Societal** | Impactos negativos en la sociedad | Deepfakes, desinformación masiva, vigilancia sin consentimiento |
| **Técnico** | Debilidades de infraestructura | APIs sin autenticación, configuraciones inseguras |

### Actualización Automática
- Al abrir el módulo, si pasaron más de 24 horas desde la última actualización, consulta las fuentes automáticamente.
- Botón "Actualizar ahora" para forzar la actualización.
- Panel de control con selector de intervalo (Manual, 1h, 6h, 12h, 24h).

### Normativa Colombiana Integrada

Cada vulnerabilidad incluye automáticamente las normas colombianas aplicables según su tipo:

| Tipo Vulnerabilidad | Normas Colombianas |
|---|---|
| **Adversarial** | Ley 1581/2012, Circular 007/2018 SFC, CONPES 3995/2020, Resolución MinTIC 2022 |
| **Privacidad** | Ley 1581/2012 (Art. 4,10,17), Decreto 1377/2013, Ley 1266/2008, CONPES 4069/2022 |
| **Sesgo** | Ley 1581/2012 Art. 4, CONPES 4069/2022 Eje 2, Proyecto Ley 059/2023, Decreto 1081/2015 |
| **Seguridad Física** | CONPES 3995/2020, Resolución MinTIC 2022, Ley 2195/2022, CONPES 4069/2022 |
| **Societal** | CONPES 4069/2022, Proyecto Ley 059/2023, Ley 2195/2022, Ley 1712/2014 |

---

## 11. Módulo 8: Autodiagnóstico

### Propósito
Encuesta de autoevaluación de madurez en gobierno de IA, basada en los requisitos de ISO 42001:2023 y NIST AI RMF.

### ¿Cómo funciona?
1. Responde una serie de preguntas organizadas por dimensiones.
2. La herramienta calcula el nivel de madurez para cada dimensión.
3. Genera un reporte con recomendaciones para avanzar al siguiente nivel.

### Niveles de Madurez
| Nivel | Descripción |
|---|---|
| **1 - Inicial** | Sin procesos definidos |
| **2 - Repetible** | Procesos informales, dependen de personas clave |
| **3 - Definido** | Procesos documentados y estandarizados |
| **4 - Gestionado** | Procesos medidos y controlados |
| **5 - Optimizado** | Mejora continua automatizada |

---

## 12. Módulo 9: Dashboard

### Propósito
Vista consolidada de todas las métricas del sistema: auditorías realizadas, vulnerabilidades detectadas, estado del sistema y tendencias.

### Indicadores
- **Total de análisis** realizados en la plataforma.
- **Total de vulnerabilidades** activas en la base de conocimiento.
- **Estado del RAG** (activo/inactivo).
- **Últimas auditorías** realizadas con fecha, fuente y resultado.

---

## 13. Módulo 10: Historial

### Propósito
Registro completo de todas las auditorías realizadas en la plataforma, con posibilidad de consultar, filtrar y descargar resultados anteriores.

### Columnas
| Columna | Descripción |
|---|---|
| Fecha | Fecha y hora de la auditoría |
| Usuario | Quién realizó la auditoría |
| Fuente | PDF, Texto Libre o Confluencia |
| Documento | Nombre del documento analizado |
| Conformes | Controles que cumplen |
| Parciales | Controles con cumplimiento parcial |
| No Conformes | Controles que no cumplen |
| Cumplimiento | Porcentaje global |
| Descargar | Enlace para descargar el reporte |

---

## 14. Módulo 11: Guía del Auditor

### Propósito
Guía interactiva para auditores basada en ISO 19011:2018 (Directrices para la auditoría de sistemas de gestión) e ISO 23894:2023 (Gestión de riesgos de IA).

### Contenido
- **Principios de auditoría** (ISO 19011): Integridad, presentación imparcial, debido cuidado profesional, confidencialidad, independencia, enfoque basado en evidencia.
- **Gestión de un programa de auditoría**: Establecimiento, implementación, monitoreo y revisión.
- **Técnicas de auditoría para IA**: Cómo auditar sistemas de IA, qué preguntar, qué evidencias buscar.
- **Listas de verificación**: Check lists para auditorías de ISO 42001 y NIST AI RMF.

---

## 15. Módulo 12: Rol del Auditor

### Propósito
Define el perfil, competencias y responsabilidades del auditor de IA según ISO 19011:2018 e ISO 23894:2023.

### Contenido
- **Competencias del auditor**: Conocimiento de IA, gestión de riesgos, normativas aplicables.
- **Responsabilidades**: Planificar, ejecutar, reportar y dar seguimiento a las auditorías.
- **Conducta profesional**: Código de ética, confidencialidad, objetividad.
- **Base de conocimiento**: Documentación de referencia para el auditor.

---

## 16. Módulo 13: Logs de Auditoría

### Propósito
Registro detallado de todas las acciones realizadas en la plataforma: inicios de sesión, auditorías ejecutadas, exportaciones, errores del sistema.

### Columnas
| Columna | Descripción |
|---|---|
| Timestamp | Fecha y hora del evento |
| Usuario | Usuario que realizó la acción |
| Acción | Tipo de evento (LOGIN, ANALYSIS, EXPORT, ERROR) |
| Resultado | Éxito o fallo |
| Detalle | Información adicional |

### Caso de uso
Un auditor jefe revisa los logs para verificar que su equipo está usando la herramienta correctamente y que no hay intentos de acceso no autorizados.

---

## 17. Base de Conocimiento de Vulnerabilidades IA

### Arquitectura

```
                        ┌─────────────────┐
                        │   Fuentes Reales │
                        │                  │
     ┌──────────────────┤ MITRE ATLAS      │
     │                  │ AVID             │
     │  Consulta cada   │ MIT AI Risk      │
     │  24h automática  │ AI Incident DB   │
     │                  │ NVD (opcional)   │
     │                  └────────┬────────┘
     │                           │
     ▼                           ▼
┌─────────────┐         ┌─────────────────┐
│ Normalizador│◄────────│   DeepSeek /    │
│  (español)  │         │  Modo Local     │
└──────┬──────┘         └─────────────────┘
       │
       ▼
┌─────────────┐         ┌─────────────────┐
│   SQLite    │────────►│  Excel Respaldo │
│  (153+      │         │  (6 pestañas)   │
│  registros) │         └─────────────────┘
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│   UI Streamlit: Tablero, Gráficos,      │
│   Detalle, Exportación                   │
└─────────────────────────────────────────┘
```

### Cálculo del Riesgo (Matriz 5×5)

```
Riesgo = Probabilidad × Severidad

Donde:
- Probabilidad (1-5): 1=Muy Baja, 2=Baja, 3=Media, 4=Alta, 5=Muy Alta
- Severidad (1-5):  1=Muy Baja, 2=Baja, 3=Media, 4=Alta, 5=Muy Alta
```

| Probabilidad \ Severidad | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | 5 | 10 | 15 | 20 | **25** |
| **4** | 4 | 8 | 12 | **16** | **20** |
| **3** | 3 | 6 | **9** | **12** | **15** |
| **2** | 2 | **4** | **6** | **8** | **10** |
| **1** | **1** | **2** | **3** | **4** | **5** |

**Niveles de Riesgo:**
- **BAJO** (1-5): Riesgo aceptable. Controles existentes suficientes.
- **MEDIO** (6-11): Riesgo tolerable. Monitoreo y mejora planificada.
- **ALTO** (12-19): Riesgo inaceptable. Acciones correctivas inmediatas.
- **EXTREMO** (20-25): Riesgo crítico. Escalamiento a dirección.

**Criticidad compuesta (0-100%):**
```
Criticidad = ((Probabilidad + Severidad) / 10) × 100
```

---

## 18. Exportación de Resultados

### Excel de Matriz de Riesgos IA (6 pestañas)

Cuando haces clic en "Generar Excel Matriz de Riesgos", obtienes un archivo con:

| Pestaña | Contenido |
|---|---|
| **Tablero de Control** | Métricas: total, extremos, altos, medios, bajos, criticidad promedio, distribución por fuente y tipo |
| **Metodología** | Marco normativo, fuentes de datos, clasificación, cálculo del riesgo, normativa colombiana |
| **Catálogo de Vulnerabilidades** | Lista completa con ID, fuente, descripción, causa raíz, cómo se ejecuta el ataque, cómo prevenirlo, solución, clasificación, táctica MITRE, probabilidad, severidad, nivel de riesgo, normas aplicables, normativa colombiana |
| **Clasificación por Táctica** | Vulnerabilidades agrupadas por código de táctica MITRE con descripción, cantidad, riesgo promedio y porcentaje |
| **Mapa de Calor P×S** | Matriz visual 5×5 coloreada con leyenda explicativa |
| **Controles y Normas Aplicables** | Cada vulnerabilidad con control recomendado, normas aplicables, tipo, prioridad, nivel de riesgo, normativa colombiana |

### Otros formatos de exportación
| Módulo | Formatos |
|---|---|
| Auditoría de IA | PDF, Markdown, TXT |
| Interoperabilidad | Excel (5 pestañas) |
| Matriz de Riesgos IA | Excel (6 pestañas), SQLite |
| Historial | Markdown, JSON |

---

## 19. Preguntas Frecuentes

### ¿Necesito conexión a Internet?
Sí, para consultar las fuentes de vulnerabilidades (MITRE ATLAS, AVID, etc.) y para usar los modelos de IA. El normalizador local funciona offline pero con descripciones genéricas.

### ¿Puedo agregar más fuentes de vulnerabilidades?
Sí. El archivo `ingestor/sources.py` está diseñado para ser extendido. Solo necesitas crear una nueva función `fetch_mi_fuente()` siguiendo el patrón de las existentes y agregarla al orquestador `fetch_all()`.

### ¿Los datos de vulnerabilidades son reales?
Sí. MITRE ATLAS descarga el YAML oficial del repositorio GitHub de MITRE. AVID descarga JSON del repositorio GitHub oficial. AI Incident Database consulta el RSS feed público. No hay datos mock ni inventados.

### ¿Cómo se traducen las vulnerabilidades a español?
Puedes configurar `DEEPSEEK_API_KEY` en `.env` para que DeepSeek traduzca y explique cada vulnerabilidad en español con lenguaje sencillo. Si no hay API key, el normalizador local genera descripciones en español usando reglas lingüísticas predefinidas.

### ¿Puedo personalizar el cuestionario contextual?
Sí. El archivo `ingestor/context_prompt.py` contiene las 11 preguntas. Puedes agregar, modificar o eliminar preguntas según las necesidades de tu organización.

### ¿Dónde se almacenan los datos?
En SQLite, archivo `data/reportes.db`. También se genera un Excel de respaldo en `data/Matriz_Riesgos_IA.xlsx` cada vez que se actualiza el feed.

### ¿Cómo programo la actualización automática?
La herramienta ya tiene actualización automática cada 24 horas al abrir el módulo de Matriz de Riesgos IA. También puedes hacer clic en "Actualizar ahora" manualmente.
