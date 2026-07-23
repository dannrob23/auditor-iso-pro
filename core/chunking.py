"""
División inteligente de documentos ISO/NIST en chunks.
Respeta la estructura de numerales (4.1, A.8.2, 6.1.2) para no partir secciones normativas.
"""
import re
from pathlib import Path
import pypdf


def chunk_document(text: str, source: str, chunk_size: int = 800, overlap: int = 150) -> list[dict]:
    """
    Divide un texto normativo en chunks respetando secciones ISO.

    Args:
        text: Texto completo del documento
        source: Nombre del archivo fuente
        chunk_size: Tamaño objetivo en palabras (~tokens)
        overlap: Solapamiento entre chunks consecutivos

    Returns:
        List[Dict] con {"text": str, "source": str, "section": str}
    """
    if not text.strip():
        return []

    # 1. Dividir por numerales ISO (A.8.8, 6.1.2, 4.1, Anexo A, etc.)
    section_pattern = re.compile(
        r'(?=\n(?:[A-Z]\.)?\d+(?:\.\d+)*[\.\s])|(?=\n[Aa]nexo\s+[A-Z])|(?=\n\d+\.\s+(?:Introducción|Objeto|Términos|Aplicabilidad))'
    )
    raw_sections = section_pattern.split(text)

    chunks = []
    current_section = "General"
    buffer = []

    for part in raw_sections:
        part = part.strip()
        if not part:
            continue

        # Detectar si esta parte inicia una nueva sección
        section_match = re.match(
            r'^((?:[A-Z]\.)?\d+(?:\.\d+)*)\s*(.*?)(?:\n|$)',
            part
        )
        if section_match:
            current_section = section_match.group(1)

        # Dividir la parte en palabras y generar chunks
        words = part.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            if len(chunk_text) > 50:  # Ignorar fragmentos muy cortos
                chunks.append({
                    "text": chunk_text,
                    "source": source,
                    "section": current_section,
                })

            # Si es el primer chunk de esta sección, incluir solapamiento con sección anterior
            if i == 0 and buffer:
                prev_chunk = buffer[-1]
                combined = prev_chunk["text"] + " " + chunk_text
                if len(combined.split()) <= chunk_size + overlap:
                    chunks.append({
                        "text": combined,
                        "source": source,
                        "section": f"{prev_chunk['section']} → {current_section}",
                    })

        buffer = [{"text": chunk_text, "source": source, "section": current_section}]

    return chunks


def _extraer_texto_pdf(ruta: Path) -> str:
    """Extrae texto de un PDF usando pypdf con manejo de errores."""
    try:
        lector = pypdf.PdfReader(str(ruta))
        texto = []
        for pagina in lector.pages:
            t = pagina.extract_text()
            if t:
                texto.append(t)
        resultado = "\n".join(texto)
        if len(resultado) < 50:
            return ""
        return resultado
    except Exception as e:
        print(f"[RAG Chunking] PDF ignorado: {ruta.name} - {e}")
        return ""


def load_and_chunk_pdfs(kb_dir: str = "knowledge_base") -> list[dict]:
    """
    Carga todos los PDFs de un directorio y los divide en chunks.

    Args:
        kb_dir: Ruta al directorio con los PDFs

    Returns:
        List[Dict] con {"text", "source", "section"}
    """
    kb_path = Path(kb_dir)
    if not kb_path.exists():
        print(f"[RAG Chunking] Directorio {kb_dir} no existe")
        return []

    pdfs = list(kb_path.glob("*.pdf"))
    if not pdfs:
        print(f"[RAG Chunking] No se encontraron PDFs en {kb_dir}")
        return []

    all_chunks = []
    for pdf_path in pdfs:
        texto = _extraer_texto_pdf(pdf_path)
        if not texto:
            continue
        chunks = chunk_document(texto, source=pdf_path.name)
        all_chunks.extend(chunks)
        print(f"[RAG Chunking] {pdf_path.name}: {len(chunks)} chunks generados")

    print(f"[RAG Chunking] Total: {len(all_chunks)} chunks de {len(pdfs)} PDFs")
    return all_chunks
