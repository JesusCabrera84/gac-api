# API Interna

Endpoints para comunicación interna entre servicios. **Requieren rol `admin`**.

**Base URL**: `/api/v1`

---

## POST `/internal/tokens/nexus`

Genera un token PASETO v4.local para comunicación segura con el servicio Nexus.

### Descripción

Este endpoint genera un token PASETO firmado con clave simétrica que permite a GAC comunicarse de forma segura con Nexus. El token tiene una expiración corta (5 minutos) por seguridad.

### Request

**Headers**:

| Header          | Valor                    | Requerido |
|-----------------|--------------------------|-----------|
| `Authorization` | `Bearer <access_token>`  | ✅        |

> ⚠️ El usuario autenticado debe tener el rol `admin`

### Response

**Status**: `200 OK`

```json
{
  "message": "Token generated successfully",
  "data": "v4.local.eyJpbnRlcm5hbF9pZCI6IjU1MGU4NDAwLWUyOWItNDFkNC1hNzE2LTQ0NjY1NTQ0MDAwMCIsInNlcnZpY2UiOiJnYWMiLCJyb2xlIjoiTkVYVVNfQURNSU4iLCJzY29wZSI6ImludGVybmFsLW5leHVzLWFkbWluIiwiaWF0IjoiMjAyNS0xMi0wOFQxMDowMDowMCswMDowMCIsImV4cCI6IjIwMjUtMTItMDhUMTA6MDU6MDArMDA6MDAifQ..."
}
```

### Payload del Token Generado

El token PASETO generado contiene los siguientes claims:

| Claim         | Tipo   | Descripción                              |
|---------------|--------|------------------------------------------|
| `internal_id` | string | UUID del usuario que generó el token     |
| `service`     | string | Servicio origen (`"gac"`)                |
| `role`        | string | Rol del token (`"NEXUS_ADMIN"`)          |
| `scope`       | string | Alcance (`"internal-nexus-admin"`)       |
| `iat`         | string | Fecha de emisión (ISO 8601)              |
| `exp`         | string | Fecha de expiración (iat + 5 minutos)    |

### Ejemplo de Payload Decodificado

```json
{
  "internal_id": "550e8400-e29b-41d4-a716-446655440000",
  "service": "gac",
  "role": "NEXUS_ADMIN",
  "scope": "internal-nexus-admin",
  "iat": "2025-12-08T10:00:00+00:00",
  "exp": "2025-12-08T10:05:00+00:00"
}
```

### Errores

| Status | Descripción                                    |
|--------|------------------------------------------------|
| `403`  | Usuario no autenticado o sin rol `admin`       |

### Ejemplo cURL

```bash
curl -X POST "http://localhost:8000/api/v1/internal/tokens/nexus" \
  -H "Authorization: Bearer <admin_access_token>"
```

### Ejemplo de Uso en Python

```python
import httpx

# 1. Obtener token PASETO
response = httpx.post(
    "http://localhost:8000/api/v1/internal/tokens/nexus",
    headers={"Authorization": f"Bearer {admin_token}"}
)
paseto_token = response.json()["data"]

# 2. Usar el token para comunicarse con Nexus
nexus_response = httpx.get(
    "http://nexus-service/api/v1/some-endpoint",
    headers={"Authorization": f"Bearer {paseto_token}"}
)
```

### Validación del Token en Nexus (Python)

```python
import pyseto
from pyseto import Key

# En el servicio Nexus
secret_key = "tu-clave-secreta-compartida"
key = Key.new(version=4, purpose="local", key=secret_key)

# Decodificar y validar el token
token = pyseto.decode(key, paseto_token)
payload = token.payload  # dict con los claims
```

---

## Configuración Requerida

Para que este endpoint funcione correctamente, se debe configurar la siguiente variable de entorno:

| Variable           | Descripción                                      |
|--------------------|--------------------------------------------------|
| `PASETO_SECRET_KEY`| Clave simétrica de 32 bytes (64 caracteres hex)  |

### Generar una clave válida

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Seguridad

- **PASETO v4.local**: Usa cifrado simétrico (XChaCha20-Poly1305) más seguro que JWT
- **Expiración corta**: El token expira en 5 minutos para minimizar el impacto de una filtración
- **Restricción de rol**: Solo usuarios con rol `admin` pueden generar estos tokens
- **Clave compartida**: La misma `PASETO_SECRET_KEY` debe configurarse en GAC y Nexus

---

## Diagrama de Flujo

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Cliente   │      │   GAC API   │      │    Nexus    │
│   (Admin)   │      │             │      │   Service   │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       │ POST /internal/    │                    │
       │ tokens/nexus       │                    │
       │ ─────────────────► │                    │
       │                    │                    │
       │   paseto_token     │                    │
       │ ◄───────────────── │                    │
       │                    │                    │
       │                    │ Request +          │
       │                    │ paseto_token       │
       │                    │ ─────────────────► │
       │                    │                    │
       │                    │     Response       │
       │                    │ ◄───────────────── │
       │                    │                    │
```

---

## Diferencias entre JWT y PASETO

| Característica      | JWT                    | PASETO                     |
|---------------------|------------------------|----------------------------|
| Algoritmo           | Configurable (riesgoso)| Fijo por versión (seguro)  |
| Cifrado local       | No nativo              | v4.local (XChaCha20)       |
| Vulnerabilidades    | Múltiples conocidas    | Diseño resistente          |
| Tamaño del token    | Más pequeño            | Ligeramente mayor          |

