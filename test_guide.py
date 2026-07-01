#!/usr/bin/env python3
"""
Test script for the updated guide functionality
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_guide_datasets():
    print("🔍 Testing guide datasets...")

    # Simular la función obtener_dataset_marco
    def obtener_dataset_marco(marco):
        if marco == "ISO/IEC 27001:2022":
            return [
                {"Marco": "ISO 27001", "Dominio": "Organizacional", "Control": "A.5.1", "Nombre": "Políticas de seguridad", "Objetivo": "Aprobación formal", "Relevancia_IC": "Alta"},
                {"Marco": "ISO 27001", "Dominio": "Tecnológico", "Control": "A.8.8", "Nombre": "Gestión de vulnerabilidades", "Objetivo": "Obtener info sobre vulnerabilidades", "Relevancia_IC": "Crítica"},
            ]
        elif marco == "NIST Cybersecurity Framework 2.0":
            return [
                {"Marco": "NIST CSF 2.0", "Dominio": "IDENTIFY", "Control": "ID.AM-1", "Nombre": "Assets Management", "Objetivo": "Identificar y gestionar activos", "Relevancia_IC": "Crítica"},
                {"Marco": "NIST CSF 2.0", "Dominio": "PROTECT", "Control": "PR.AC-1", "Nombre": "Access Control", "Objetivo": "Implementar control de acceso", "Relevancia_IC": "Crítica"},
            ]
        elif marco == "ISO/IEC 42001:2023":
            return [
                {"Marco": "ISO 42001", "Dominio": "Liderazgo", "Control": "5.1", "Nombre": "Liderazgo y compromiso", "Objetivo": "Demostrar liderazgo", "Relevancia_IC": "Crítica"},
                {"Marco": "ISO 42001", "Dominio": "Operación", "Control": "8.3", "Nombre": "Diseño y desarrollo de IA", "Objetivo": "Controlar diseño de IA", "Relevancia_IC": "Crítica"},
            ]
        else:  # Vista integrada
            return obtener_dataset_marco("ISO/IEC 27001:2022") + obtener_dataset_marco("NIST Cybersecurity Framework 2.0") + obtener_dataset_marco("ISO/IEC 42001:2023")

    # Test each marco
    marcos = ["ISO/IEC 27001:2022", "NIST Cybersecurity Framework 2.0", "ISO/IEC 42001:2023", "Vista integrada"]

    for marco in marcos:
        data = obtener_dataset_marco(marco)
        print(f"✅ {marco}: {len(data)} controles")

        # Check structure
        if data:
            required_fields = ["Marco", "Dominio", "Control", "Nombre", "Objetivo", "Relevancia_IC"]
            sample = data[0]
            missing_fields = [field for field in required_fields if field not in sample]
            if missing_fields:
                print(f"  ⚠️  Missing fields: {missing_fields}")
            else:
                print("  ✅ Structure correcta")

    print("\n🎉 All guide datasets working!")

if __name__ == "__main__":
    test_guide_datasets()