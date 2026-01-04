#!/usr/bin/env python3
"""
Script de debugging para verificar roles de usuario y configuración de base de datos.
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings


async def debug_user_and_roles():
    """Debug completo de usuario y roles"""
    print("🔧 Configuración de base de datos:")
    print(f"   Host: {settings.DB_HOST}")
    print(f"   Puerto: {settings.DB_PORT}")
    print(f"   Usuario: {settings.DB_USER}")
    print(f"   Base de datos: {settings.DB_NAME}")
    print(f"   Esquema: {settings.DB_SCHEME}")
    print()

    async for db in get_db():
        try:
            # Verificar esquema actual
            print("📋 Verificando esquema y search_path...")
            result = await db.execute(text("SHOW search_path"))
            search_path = result.scalar()
            print(f"   search_path actual: {search_path}")

            # Verificar que existan las tablas
            print("\n📊 Verificando tablas...")
            tables = ['users', 'roles', 'user_roles']
            for table in tables:
                try:
                    result = await db.execute(text(f"SELECT COUNT(*) FROM {settings.DB_SCHEME}.{table}"))
                    count = result.scalar()
                    print(f"   {settings.DB_SCHEME}.{table}: {count} registros")
                except Exception as e:
                    print(f"   ❌ Error en {settings.DB_SCHEME}.{table}: {e}")

            # Verificar usuario específico
            print("\n👤 Verificando usuario específico...")
            user_id = "9f5008c0-4c39-4da3-a3a6-c9a63a261296"

            # Consulta directa a la tabla users
            result = await db.execute(text(f"""
                SELECT user_id, email, full_name, is_active, created_at
                FROM {settings.DB_SCHEME}.users
                WHERE user_id = :user_id
            """), {"user_id": user_id})

            user = result.fetchone()
            if not user:
                print(f"   ❌ Usuario {user_id} no encontrado")
                return

            print(f"   ✅ Usuario encontrado:")
            print(f"      ID: {user.user_id}")
            print(f"      Email: {user.email}")
            print(f"      Nombre: {user.full_name}")
            print(f"      Activo: {user.is_active}")

            # Verificar roles del usuario
            print("\n🎭 Verificando roles del usuario...")
            result = await db.execute(text(f"""
                SELECT r.role_id, r.name
                FROM {settings.DB_SCHEME}.roles r
                JOIN {settings.DB_SCHEME}.user_roles ur ON r.role_id = ur.role_id
                WHERE ur.user_id = :user_id
            """), {"user_id": user_id})

            roles = result.fetchall()
            if not roles:
                print("   ❌ Usuario no tiene roles asignados")
                return

            print(f"   ✅ Usuario tiene {len(roles)} rol(es):")
            for role in roles:
                print(f"      - {role.name} (ID: {role.role_id})")

            # Verificar si tiene rol admin
            role_names = [role.name for role in roles]
            has_admin = "admin" in role_names
            print(f"\n🔐 ¿Tiene rol 'admin'? {has_admin}")

            if not has_admin:
                print("   ❌ Este es el motivo del error 403!")
                print("   ❌ El usuario no tiene el rol 'admin' necesario para acceder al endpoint")
            else:
                print("   ✅ El usuario tiene permisos de admin - el problema debe estar en otro lado")

        except Exception as e:
            print(f"❌ Error al consultar la base de datos: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()

        break


if __name__ == "__main__":
    print("🔍 Iniciando debugging de usuario y roles...")
    print("=" * 60)
    asyncio.run(debug_user_and_roles())
