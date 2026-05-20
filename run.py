#!/usr/bin/env python
"""Script simple para ejecutar la aplicación Flask."""

import asyncio
import sys
import io
from pathlib import Path

# Force UTF-8 for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import create_app

if __name__ == "__main__":
    try:
        print("Iniciando aplicación Flask...")
        app = create_app()
        print("\n✅ Aplicación iniciada correctamente")
        print("🌐 Accede en: http://localhost:5000")
        print("📊 Health check: http://localhost:5000/api/v1/health")
        print("\n✋ Presiona Ctrl+C para detener\n")
        app.run(debug=True, host="127.0.0.1", port=5000)
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
