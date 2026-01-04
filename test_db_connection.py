#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos y verificar roles de usuario.
"""
import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.config import settings
from app.models.users import User


async def test_user_roles():
    """Probar la carga de roles de usuario"""
    print(f"🔧 Usando esquema de base de datos: {settings.DB_SCHEME}")

    async for db in get_db():
        try:
            # Consultar el usuario específico
            user_id = "9f5008c0-4c39-4da3-a3a6-c9a63a261296"
            stmt = (
                select(User)
                .options(selectinload(User.roles))
                .where(User.user_id == user_id)
            )

            result = await db.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                print(f"❌ Usuario {user_id} no encontrado")
                return

            print(f"✅ Usuario encontrado: {user.email}")
            print(f"   Nombre: {user.full_name}")
            print(f"   Activo: {user.is_active}")

            print(f"   Roles encontrados: {len(user.roles)}")
            for role in user.roles:
                print(f"     - {role.name} (ID: {role.role_id})")

            # Verificar si tiene rol admin
            role_names = [role.name for role in user.roles]
            has_admin = "admin" in role_names
            print(f"   ¿Tiene rol admin? {has_admin}")

        except Exception as e:
            print(f"❌ Error al consultar la base de datos: {e}")
            return

        break  # Solo necesitamos una sesión


if __name__ == "__main__":
    print("🔍 Probando conexión a la base de datos...")
    asyncio.run(test_user_roles())
