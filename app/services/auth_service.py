from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from pydantic import ValidationError

from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.users import User
from app.schemas.auth import Token, TokenPayload


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password_hash):
            return None

        if not user.is_active:
            return None

        # Update last login
        user.last_login_at = datetime.utcnow()
        await self.db.commit()

        access_token = create_access_token(subject=user.user_id)
        refresh_token = create_refresh_token(subject=user.user_id)

        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    async def refresh_token(self, refresh_token: str) -> Optional[Token]:
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            token_data = TokenPayload(**payload)

            if token_data.type != "refresh":
                return None

        except (JWTError, ValidationError):
            return None

        stmt = select(User).where(User.user_id == token_data.sub)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            return None

        new_access_token = create_access_token(subject=user.user_id)
        # Optionally rotate refresh token here, for now just return new access token
        # Returning the same refresh token or a new one depends on policy.
        # Requirement says "refresh token (7-30 days)", usually implies reuse until expiry or rotation.
        # Let's issue a new access token only as per typical flow, or both.
        # The prompt asked for "POST /api/v1/auth/refresh", usually returns new access token.

        return Token(
            access_token=new_access_token,
            refresh_token=refresh_token,  # Return same refresh token or rotate
            token_type="bearer",
        )
