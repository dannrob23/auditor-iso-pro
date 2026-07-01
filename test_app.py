#!/usr/bin/env python3
"""
Test script for the application without Streamlit
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_imports():
    print("🔍 Testing imports and basic functionality...")

    try:
        # Test basic imports
        from interoperabilidad import obtener_dimensiones, obtener_sector
        print("✅ interoperabilidad module imported")

        # Test data
        dims = obtener_dimensiones()
        print(f"✅ Dimensions loaded: {len(dims)}")

        sector = obtener_sector('energia')
        if sector:
            print(f"✅ Sector data loaded: {sector['nombre']}")

        # Test RAG (with error handling)
        try:
            from rag_knowledge import base_conocimiento_activa
            rag_status = base_conocimiento_activa()
            print(f"✅ RAG status: {rag_status}")
        except Exception as e:
            print(f"⚠️  RAG not available: {e}")

        print("\n🎉 All core functionality working!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_imports()