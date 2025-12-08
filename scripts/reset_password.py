import asyncio
import sys
import os
from sqlalchemy import select

# Add project root to path
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.users import User
from app.core.security import get_password_hash


async def reset_password():
    email = "gac-admin@geminislabs.com"
    new_password = "gac-admin"

    print(f"Resetting password for {email}...")

    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            print(f"User found. Current hash start: {user.password_hash[:20]}...")

            new_hash = get_password_hash(new_password)
            print(f"New hash generated: {new_hash[:20]}...")

            user.password_hash = new_hash
            await session.commit()
            print("Password updated successfully.")
        else:
            print(f"User {email} not found.")


if __name__ == "__main__":
    try:
        asyncio.run(reset_password())
    except Exception as e:
        print(f"Error: {e}")
