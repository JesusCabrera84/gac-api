import base64
import json
import uuid
from datetime import datetime, timedelta, timezone

import pyseto
from pyseto import Key

from app.core.config import settings


def create_app_token(
    user_id: uuid.UUID, app_name: str = "gac", expires_in_minutes: int = 5
) -> str:
    """
    Crea un token PASETO v4.local para comunicación interna de aplicaciones.

    Args:
        user_id: UUID del usuario que solicita el token
        app_name: Nombre de la aplicación (default: "gac")
        expires_in_minutes: Tiempo de expiración en minutos (default: 5)

    Returns:
        Token PASETO codificado
    """
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_in_minutes)

    payload = {
        "internal_id": str(user_id),
        "service": app_name,
        "role": f"{app_name.upper()}_ADMIN",
        "scope": f"internal-{app_name}-admin",
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

    # Convertir payload a JSON string para compatibilidad
    payload_json = json.dumps(payload, separators=(",", ":"))

    token = pyseto.encode(key, payload_json.encode("utf-8"))

    return token.decode("utf-8") if isinstance(token, bytes) else token


def decode_app_token(token: str) -> dict:
    """
    Decodifica y valida un token PASETO de aplicación.

    Args:
        token: Token PASETO a decodificar

    Returns:
        Payload decodificado del token

    Raises:
        ValueError: Si el token es inválido o ha expirado
    """
    try:
        # Decodificar la clave desde base64 (debe ser de 32 bytes)
        secret = base64.b64decode(settings.PASETO_SECRET_KEY)
        if len(secret) < 32:
            secret = secret.ljust(32, b"\0")
        elif len(secret) > 32:
            secret = secret[:32]

        key = Key.new(version=4, purpose="local", key=secret)
        decoded = pyseto.decode(key, token)

        # Decodificar el payload como hace el otro API
        payload = json.loads(decoded.payload.decode("utf-8"))

        # Verificar expiración
        if isinstance(payload, dict) and "exp" in payload:
            exp_datetime = datetime.fromisoformat(payload["exp"])
            if exp_datetime < datetime.now(timezone.utc):
                raise ValueError("Token has expired")

        return payload

    except Exception as e:
        raise ValueError(f"Invalid token: {str(e)}")


def refresh_app_token(
    token: str, app_name: str = "gac", expires_in_minutes: int = 5
) -> str:
    """
    Refresca un token PASETO existente generando uno nuevo con la misma información.

    Args:
        token: Token PASETO existente a refrescar
        app_name: Nombre de la aplicación (default: "gac")
        expires_in_minutes: Nuevo tiempo de expiración en minutos (default: 5)

    Returns:
        Nuevo token PASETO

    Raises:
        ValueError: Si el token original es inválido
    """
    try:
        payload = decode_app_token(token)
        user_id = uuid.UUID(payload["internal_id"])
        return create_app_token(user_id, app_name, expires_in_minutes)
    except Exception as e:
        raise ValueError(f"Cannot refresh token: {str(e)}")


def decode_service_token(
    token: str,
    required_service: str | None = None,
    required_role: str | None = None,
) -> dict | None:
    """
    Decodifica y valida un token PASETO de servicio (compatible con otros servicios).

    Args:
        token: Token PASETO a decodificar
        required_service: Si se proporciona, valida que el service coincida
        required_role: Si se proporciona, valida que el role coincida

    Returns:
        dict: Payload del token si es válido, None si es inválido o expirado
    """
    try:
        # Decodificar la clave desde base64 (debe ser de 32 bytes)
        secret = base64.b64decode(settings.PASETO_SECRET_KEY)
        if len(secret) < 32:
            secret = secret.ljust(32, b"\0")
        elif len(secret) > 32:
            secret = secret[:32]

        key = Key.new(version=4, purpose="local", key=secret)
        decoded = pyseto.decode(key, token)

        # Decodificar el payload como JSON (compatible con otros servicios)
        payload = json.loads(decoded.payload.decode("utf-8"))

        # Validar expiración
        exp = datetime.fromisoformat(payload["exp"])
        if datetime.now(timezone.utc) > exp:
            return None

        # Validar scope - aceptar scopes de servicio válidos
        valid_service_scopes = {
            "service-auth",
            "internal-nexus-admin",
            "internal-gac-admin",
            "internal-app-admin",
        }
        scope = payload.get("scope")
        if scope and scope not in valid_service_scopes:
            # Ser más flexible: si tiene service="gac", aceptar cualquier scope que empiece con "internal"
            if payload.get("service") == "gac" and scope.startswith("internal"):
                pass  # Aceptar
            else:
                return None

        # Validar service si se requiere
        if required_service and payload.get("service") != required_service:
            return None

        # Validar role si se requiere
        if required_role and payload.get("role") != required_role:
            return None

        return payload

    except Exception:
        return None
