import uuid
from datetime import datetime, timedelta, timezone

import pyseto
from pyseto import Key

from app.core.config import settings


def create_nexus_token(user_id: uuid.UUID, expires_in_minutes: int = 5) -> str:
    """
    Crea un token PASETO v4.local para comunicación con Nexus.

    Args:
        user_id: UUID del usuario que solicita el token
        expires_in_minutes: Tiempo de expiración en minutos (default: 5)

    Returns:
        Token PASETO codificado
    """
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_in_minutes)

    payload = {
        "internal_id": str(user_id),
        "service": "gac",
        "role": "NEXUS_ADMIN",
        "scope": "internal-nexus-admin",
        "iat": now.isoformat(),
        "exp": exp.isoformat(),
    }

    # Crear clave simétrica para v4.local
    key = Key.new(version=4, purpose="local", key=settings.PASETO_SECRET_KEY)

    token = pyseto.encode(key, payload)

    return token.decode("utf-8") if isinstance(token, bytes) else token
