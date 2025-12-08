import asyncio
import sys
import os
from sqlalchemy import select

# Add project root to path
sys.path.append(os.getcwd())

from app.core.database import AsyncSessionLocal
from app.models.users import User


async def check_user_hash():
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.email == "gac-admin@geminislabs.com")
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            print(f"User found: {user.email}")
            print(f"Password hash: '{user.password_hash}'")
            print(f"Hash type: {type(user.password_hash)}")
            print(
                f"Hash length: {len(user.password_hash) if user.password_hash else 0}"
            )
        else:
            print("User not found")


if __name__ == "__main__":
    asyncio.run(check_user_hash())
