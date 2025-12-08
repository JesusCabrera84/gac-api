import base64
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
    """
    Inicializa el generador con la clave secreta de la configuración.
    La clave debe ser de 32 bytes para PASETO v4.local.
    """
    # Decodificar la clave desde base64 (debe ser de 32 bytes)
    secret = base64.b64decode(settings.PASETO_SECRET_KEY)
    if len(secret) < 32:
        # Pad con ceros si es menor
        secret = secret.ljust(32, b"\0")
    elif len(secret) > 32:
        # Truncar si es mayor
        secret = secret[:32]

    key = Key.new(version=4, purpose="local", key=secret)

    token = pyseto.encode(key, payload)

    return token.decode("utf-8") if isinstance(token, bytes) else token
