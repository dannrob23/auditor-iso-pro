#!/usr/bin/env python3
"""
Script para regenerar el índice FAISS si hay problemas
Ejecutar desde el directorio del proyecto con el entorno virtual activado
"""

import sys
import os
from pathlib import Path

# Agregar directorio actual al path
sys.path.insert(0, os.getcwd())

def regenerar_indice():
    print("🔄 Regenerando índice FAISS...")
    print("=" * 50)

    try:
        from rag_knowledge import indexar_documentos, DB_DIR
        import shutil

        # Eliminar índice existente si existe
        if DB_DIR.exists():
            print(f"Eliminando índice existente en {DB_DIR}")
            shutil.rmtree(DB_DIR)

        # Crear nuevo índice
        print("Creando nuevo índice...")
        num_chunks, mensaje = indexar_documentos()

        if num_chunks > 0:
            print(f"✅ Índice regenerado exitosamente: {num_chunks} fragmentos")
            print(f"📝 {mensaje}")
        else:
            print(f"❌ Error al regenerar índice: {mensaje}")

    except Exception as e:
        print(f"❌ Error durante la regeneración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    regenerar_indice()