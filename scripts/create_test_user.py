import asyncio
import sys
import os
from sqlalchemy import select
from passlib.context import CryptContext

# Add project root to path
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.users import User, Role, UserRole
from app.core.security import get_password_hash


async def create_test_user():
    async with AsyncSessionLocal() as session:
        # Check if user exists
        stmt = select(User).where(User.email == "admin@gac.com")
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            print("Creating test user...")
            user = User(
                email="admin@gac.com",
                password_hash=get_password_hash("admin123"),
                full_name="Admin User",
                is_active=True,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"User created: {user.user_id}")

            # Create admin role if not exists
            stmt = select(Role).where(Role.name == "admin")
            result = await session.execute(stmt)
            role = result.scalar_one_or_none()
            if not role:
                role = Role(name="admin")
                session.add(role)
                await session.commit()
                await session.refresh(role)

            # Assign role
            user_role = UserRole(user_id=user.user_id, role_id=role.role_id)
            session.add(user_role)
            await session.commit()
            print("Admin role assigned")
        else:
            print("Test user already exists")


if __name__ == "__main__":
    try:
        asyncio.run(create_test_user())
    except Exception as e:
        print(f"Error: {e}")
