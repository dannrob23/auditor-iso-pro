# 🔐 Auditor ISO/IEC 27001:2022 — Gap Analysis IA

Aplicación web para realizar Gap Analysis automatizados sobre políticas de seguridad de la información usando IA (GPT-4o, DeepSeek, Google Gemini o Groq gratuito).

## ✨ Características

- 🔒 **Autenticación segura** con `streamlit-authenticator`
- 📄 **Análisis de PDFs** — sube tu política y extrae el texto automáticamente
- ✏️ **Texto libre** — pega el texto directamente
- 🤖 **IA auditora** — GPT-4o, DeepSeek, Gemini o Groq (gratis) como Auditor Líder ISO 27001:2022
- 📊 **Tabla de Gap Analysis** con estado de evidencia y acciones correctivas
- ⬇️ **Descarga el reporte** en formato Markdown o PDF

## 🚀 Instalación local

```bash
git clone https://github.com/tu-usuario/auditor-iso-pro.git
cd auditor-iso-pro
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Configuración

1. Copia el archivo de ejemplo y agrega tu API Key:
```bash
cp .env.example .env
# Edita .env con al menos una API Key
```

2. (Opcional) Cambia usuarios/contraseñas en `config.yaml`:
```bash
# Genera un hash de contraseña con:
python -c "import streamlit_authenticator as sa; print(sa.Hasher(['TuContraseña']).generate())"
```

**Credenciales por defecto:**
- Usuario: `auditor` | Contraseña: `Auditor2024!`

## 👉 Proveedores de IA soportados

| Proveedor | Modelos | Costo |
|-----------|---------|-------|
| **Groq** | llama-3.3-70b, mixtral | **Gratis** |
| DeepSeek | deepseek-chat | Pago |
| Google (Gemini) | gemini-1.5-pro/flash | Pago |
| OpenAI | gpt-4o, gpt-4-turbo | Pago |

> **Recomendación:** Usa **Groq (Gratis)** para probar la app sin costo.

## ▶️ Ejecutar

```bash
streamlit run app.py
```

## ☁️ Deploy en Streamlit Community Cloud

1. Sube el repositorio a GitHub (sin el `.env`)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. En **Advanced settings → Secrets**, agrega:
```toml
# Opción 1: Groq (Gratis) — recomendado
GROQ_API_KEY = "gsk_..."

# Opción 2: OpenAI
OPENAI_API_KEY = "sk-..."

# Opción 3: Google Gemini
GOOGLE_API_KEY = "..."

# Opción 4: DeepSeek
DEEPSEEK_API_KEY = "..."

# Cookie secret para autenticación (genera uno aleatorio)
COOKIE_SECRET = "un-string-secreto-aleatorio"
```
5. Haz clic en **Deploy**

## 📁 Estructura del proyecto

```
auditor-iso-pro/
├── app.py              # Aplicación principal
├── config.yaml         # Configuración de usuarios
├── requirements.txt    # Dependencias
├── .env.example        # Plantilla de variables de entorno
├── .gitignore          # Archivos excluidos de Git
└── README.md           # Este archivo
```

## 🛡️ Controles evaluados (Anexo A ISO 27001:2022)

| Control | Descripción |
|---------|-------------|
| A.5.1  | Políticas de seguridad |
| A.5.9  | Inventario de activos |
| A.5.15 | Control de acceso |
| A.6.3  | Concientización y formación |
| A.8.8  | Gestión de vulnerabilidades |
| A.8.15 | Registros y logs |
| A.8.24 | Criptografía |

## 📄 Licencia

MIT License
