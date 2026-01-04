#!/usr/bin/env python3
"""
Script para verificar que la configuración esté correcta.
"""
import os
from pathlib import Path

def check_env_file():
    """Verificar que el archivo .env exista"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        return False

    print("✅ Archivo .env existe")
    print("   📝 Asegúrate de que contenga:")
    print("      - DB_SCHEME=gac")
    print("      - JWT_SECRET=...")
    print("      - PASETO_SECRET_KEY=...")
    return True

def check_modified_files():
    """Verificar que los archivos modificados existan y sean recientes"""
    files_to_check = [
        "app/core/config.py",
        "app/core/database.py",
        "app/api/v1/internal.py"
    ]

    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} existe")
        else:
            print(f"❌ {file_path} no encontrado")
            return False

    return True

if __name__ == "__main__":
    print("🔍 Verificando configuración de GAC API...")
    print("=" * 50)

    env_ok = check_env_file()
    files_ok = check_modified_files()

    print()
    if env_ok and files_ok:
        print("✅ Configuración correcta!")
        print("\n📋 Próximos pasos:")
        print("1. Reinicia tu aplicación FastAPI")
        print("2. Prueba el endpoint de debugging:")
        print("   GET /api/v1/internal/debug/user")
        print("3. Si funciona, prueba el endpoint original:")
        print("   POST /api/v1/internal/tokens/app")
    else:
        print("❌ Configuración incompleta - revisa los errores arriba")
