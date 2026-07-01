#!/usr/bin/env python3
"""
Script de diagnóstico para el sistema RAG
Ejecutar desde el directorio del proyecto con el entorno virtual activado
"""

import sys
import os
from pathlib import Path

# Agregar directorio actual al path
sys.path.insert(0, os.getcwd())

def diagnosticar_rag():
    print("🔍 Diagnóstico del Sistema RAG")
    print("=" * 50)

    # Verificar estructura de directorios
    data_dir = Path("data")
    faiss_dir = data_dir / "faiss_index"
    knowledge_dir = Path("knowledge_base")

    print(f"📁 Directorio data existe: {data_dir.exists()}")
    print(f"📁 Directorio FAISS existe: {faiss_dir.exists()}")
    print(f"📁 Directorio knowledge_base existe: {knowledge_dir.exists()}")

    # Verificar archivos FAISS
    faiss_file = faiss_dir / "index.faiss"
    pkl_file = faiss_dir / "index.pkl"

    print(f"📄 index.faiss existe: {faiss_file.exists()}")
    print(f"📄 index.pkl existe: {pkl_file.exists()}")

    if faiss_file.exists():
        size_faiss = faiss_file.stat().st_size
        print(f"📊 Tamaño index.faiss: {size_faiss:,} bytes")

    if pkl_file.exists():
        size_pkl = pkl_file.stat().st_size
        print(f"📊 Tamaño index.pkl: {size_pkl:,} bytes")

    # Verificar archivos de conocimiento
    archivos_kb = []
    for ext in ['*.pdf', '*.txt', '*.docx', '*.pptx', '*.xlsx']:
        archivos_kb.extend(list(knowledge_dir.glob(ext)))

    print(f"📚 Documentos en knowledge_base: {len(archivos_kb)}")
    for archivo in archivos_kb[:5]:  # Mostrar primeros 5
        size = archivo.stat().st_size
        print(f"  - {archivo.name} ({size:,} bytes)")

    if len(archivos_kb) > 5:
        print(f"  ... y {len(archivos_kb) - 5} más")

    print("\n✅ Diagnóstico completado")

if __name__ == "__main__":
    diagnosticar_rag()