## Diapositiva 1

MITRE ATT&CK: ESTRATEGIA Y COMPORTAMIENTO DEL ADVERSARIO
Especialización en Seguridad de la Información | Análisis de TTPs y la Pirámide del Dolor
Presentado por: Jose David Vargas

---

## Diapositiva 2

¿QUÉ ES MITRE ATT&CK?
Adversarial Tactics, Techniques, and Common Knowledge (ATT&CK)Es una base de conocimiento global de tácticas y técnicas de adversarios, basada en observaciones del mundo real.
Estándar de la Industria: Lenguaje común para defensores.
Foco en el Comportamiento: No se centra en el "qué" (vulnerabilidad), sino en el "cómo" (acción).
Colaboración Global: Alimentada por la comunidad de ciberseguridad.

---

## Diapositiva 3

ENTENDIENDO LA MATRIZ
La jerarquía se completa con Sub-técnicas (detalles granulares) y Procedimientos (implementaciones reales).
TÁCTICAS
Representan el "Por Qué" del atacante. Son sus objetivos estratégicos (ej. El atacante quiere mantener el acceso aunque se reinicie el servidor (Persistencia)).
TÉCNICAS
Representan el "Cómo". Las acciones específicas que ejecutan para lograr la táctica (ej. Para lograr la Persistencia, el atacante crea una Tarea Programada.).

---

## Diapositiva 4

ENTENDIENDO LA MATRIZ
TÁCTICAS  EJEMPLOS

---

## Diapositiva 5

LAS 14 TÁCTICAS DE ENTERPRISE
RECONOCIMIENTO
Recopilar información para planificar.
ACCESO INICIAL
Entrar en la red objetivo.
PERSISTENCIA
Mantener el acceso en el tiempo.
EVASIÓN DE DEFENSA
Evitar ser detectado por el SOC.
MOVIMIENTO LATERAL
Moverse por el entorno interno.
EXFILTRACIÓN
Robar datos de interés.

---

## Diapositiva 6

ANEXOS Y RECURSOS OFICIALES
Página Oficial de MITRE ATT&CK: attack.mitre.org 

Matriz para Enterprise (Sistemas IT): Matrices - Enterprise (Es la más común, incluye Windows, Linux, Cloud).


Matriz para Sistemas de Control Industrial (ICS): Matrices - ICS (Vital si hablas de infraestructuras críticas).
Anexos Técnicos y Herramientas

ATT&CK Navigator: https://mitre-attack.github.io/attack-navigator/ 

Uso: Es una herramienta interactiva para crear capas (layers) de visualización, ideal para mostrar tu cobertura de seguridad actual.

Grupos de Adversarios: https://attack.mitre.org/groups/ 

Uso: Listado de grupos (ej. APT41, Lazarus) y las técnicas que usan frecuentemente.

Mitigaciones Relacionadas: https://attack.mitre.org/mitigations/ 

Uso: Anexo fundamental que describe cómo prevenir cada técnica (ej. endurecimiento del SO, segmentación).

---

## Diapositiva 7

LA PIRÁMIDE DEL DOLOR
Elevando el costo operativo del adversario

---

## Diapositiva 8

EL CONCEPTO DE DAVID BIANCO
Creada en 2013, define que no todos los indicadores tienen el mismo valor. La efectividad de la defensa se mide por cuánto "dolor" causamos al atacante al romper sus procesos.
La clave: Bloquear un IP es molesto; romper un TTP (Táctica, Técnica o Procedimiento) obliga al atacante a reinventarse.

---

## Diapositiva 9

COMPARATIVA DE INDICADORES

---

## Diapositiva 10

APLICACIÓN
THREAT HUNTING
Crear hipótesis de búsqueda basadas en técnicas específicas de grupos APT.
GAP ANALYSIS
Identificar qué técnicas no estamos detectando con nuestros Firewalls o EDRs.
EMULACIÓN
Simular comportamientos reales de adversarios para probar la resiliencia.

---

## Diapositiva 11

DE DATOS A INTELIGENCIA
Automatización: Los niveles bajos (Hash, IPs) deben ser bloqueados automáticamente (SOAR).
Análisis Humano: Los analistas deben enfocarse en los niveles superiores (TTPs).
Métricas de Valor: Medir cuántas tácticas de MITRE cubrimos hoy vs el mes pasado.

---

## Diapositiva 12

CASO: INFRAESTRUCTURA ELECTORAL
En sistemas críticos, el mapeo de MITRE permite:
La Pirámide del Dolor asegura que si un atacante cambia su IP, nuestra detección basada en su comportamiento (TTP) lo identifique de nuevo.
•
Detectar intentos de Acceso Inicial en bases de datos de votación.
•
Identificar Movimiento Lateral entre nodos de transmisión de resultados.
•
Bloquear Exfiltración de datos censales mediante protocolos alternativos.

---

## Diapositiva 13

RECURSOS OFICIALES
ATT&CK NAVIGATOR
Herramienta interactiva para mapear coberturas. attack.mitre.org
GRUPOS DE APT
Base de datos de actores y sus métodos favoritos.
MITIGACIONES
Guía oficial para endurecer sistemas frente a cada técnica.

---

## Diapositiva 14

¿PREGUNTAS?
"No detectes archivos, detecta comportamientos."
Gracias por su atención.

---
