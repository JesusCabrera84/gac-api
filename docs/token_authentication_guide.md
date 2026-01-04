# Guía de Autenticación - JWT vs PASETO

Esta guía explica el sistema de autenticación de la API GAC, incluyendo dónde se usan JWT y PASETO, qué endpoints requieren cada tipo de token, y cómo se construyen los tokens.

## 📋 Tabla de Contenido

- [Tokens Disponibles](#tokens-disponibles)
- [Flujo de Autenticación](#flujo-de-autenticación)
- [Endpoints por Tipo de Token](#endpoints-por-tipo-de-token)
- [Parámetros de Construcción](#parámetros-de-construcción)
- [Casos de Uso](#casos-de-uso)

---

## 🔑 Tokens Disponibles

### JWT (JSON Web Tokens)
- **Propósito**: Autenticación de usuarios en la API
- **Algoritmo**: HS256 (configurable)
- **Uso**: Autenticación principal de usuarios
- **Vigencia**: Access (30 min), Refresh (7 días)

### PASETO (Platform-Agnostic Security Tokens)
- **Propósito**: Comunicación segura entre servicios
- **Algoritmo**: XChaCha20-Poly1305 (fijo)
- **Uso**: Tokens temporales para comunicación inter-servicios
- **Vigencia**: 5 minutos (configurable)

---

## 🔄 Flujo de Autenticación

```
1. Login ──────► JWT Access + Refresh
    │
    └─► Refresh ───► Nuevo JWT Access + Refresh
                      │
                      └─► Generar PASETO ──► Token PASETO para servicios
                                      │
                                      └─► Refresh PASETO ──► Nuevo Token PASETO
```

---

## 📍 Endpoints por Tipo de Token

### 🔓 Endpoints Públicos (Sin Token)

#### POST `/api/v1/auth/login`
- **Autenticación**: Ninguna
- **Propósito**: Login de usuario
- **Body**: `username` (email), `password`
- **Respuesta**: JWT Access + Refresh tokens

### 🔐 Endpoints que requieren JWT

#### POST `/api/v1/auth/refresh`
- **Token requerido**: JWT Refresh (en query param)
- **Propósito**: Generar nuevos tokens JWT
- **Respuesta**: Nuevos JWT Access + Refresh

#### GET `/api/v1/auth/me`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Obtener información del usuario actual
- **Respuesta**: Datos del usuario autenticado

#### PATCH `/api/v1/auth/password`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Cambiar contraseña del usuario actual
- **Respuesta**: Confirmación de cambio

#### POST `/api/v1/orders`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Crear nueva orden
- **Respuesta**: Orden creada

#### GET `/api/v1/orders`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Listar órdenes del usuario
- **Respuesta**: Lista de órdenes

#### GET `/api/v1/orders/{order_id}`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Obtener orden específica
- **Respuesta**: Detalles de la orden

#### POST `/api/v1/payments`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Procesar pago
- **Respuesta**: Confirmación de pago

#### GET `/api/v1/payments`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Listar pagos del usuario
- **Respuesta**: Lista de pagos

#### GET `/api/v1/payments/{payment_id}`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Obtener pago específico
- **Respuesta**: Detalles del pago

#### GET `/api/v1/devices`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Listar dispositivos
- **Respuesta**: Lista de dispositivos

#### GET `/api/v1/products`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Listar productos
- **Respuesta**: Lista de productos

#### POST `/api/v1/products`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Crear producto
- **Respuesta**: Producto creado

#### POST `/api/v1/shipments`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Crear envío
- **Respuesta**: Envío creado

#### PATCH `/api/v1/shipments/{shipment_id}`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Actualizar envío
- **Respuesta**: Envío actualizado

#### GET `/api/v1/shipments`
- **Token requerido**: JWT Access (en header Authorization)
- **Propósito**: Listar envíos
- **Respuesta**: Lista de envíos

### 👑 Endpoints que requieren JWT + Rol Admin

#### POST `/api/v1/users`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Crear nuevo usuario
- **Respuesta**: Usuario creado

#### GET `/api/v1/users`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Listar todos los usuarios
- **Respuesta**: Lista de usuarios

#### GET `/api/v1/users/{user_id}`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Obtener usuario específico
- **Respuesta**: Detalles del usuario

#### PATCH `/api/v1/users/{user_id}`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Actualizar usuario
- **Respuesta**: Usuario actualizado

#### DELETE `/api/v1/users/{user_id}`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Desactivar usuario
- **Respuesta**: Confirmación

#### PATCH `/api/v1/users/{user_id}/password`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Cambiar contraseña de usuario
- **Respuesta**: Confirmación

#### POST `/api/v1/roles`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Crear nuevo rol
- **Respuesta**: Rol creado

#### GET `/api/v1/roles`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Listar roles
- **Respuesta**: Lista de roles

#### POST `/api/v1/roles/assign`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Asignar rol a usuario
- **Respuesta**: Confirmación

#### DELETE `/api/v1/roles/{role_id}`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Eliminar rol
- **Respuesta**: Confirmación

### 🔒 Endpoints que requieren JWT Admin + generan PASETO

#### POST `/api/v1/internal/tokens/app`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Generar token PASETO para aplicación
- **Respuesta**: Token PASETO

#### POST `/api/v1/internal/tokens/refresh`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Refrescar token PASETO existente
- **Respuesta**: Nuevo token PASETO

#### GET `/api/v1/internal/debug/user`
- **Token requerido**: JWT Access (en header Authorization)
- **Rol requerido**: `admin`
- **Propósito**: Debug de información del usuario
- **Respuesta**: Información de debugging

---

## 🛠️ Parámetros de Construcción

### JWT Access Token

**Función**: `create_access_token(subject: str)`

**Parámetros de construcción**:
- `sub`: UUID del usuario (string)
- `exp`: Timestamp de expiración (30 minutos por defecto)
- `type`: Siempre `"access"`

**Payload resultante**:
```json
{
  "sub": "9f5008c0-4c39-4da3-a3a6-c9a63a261296",
  "exp": 1735666800,
  "type": "access"
}
```

### JWT Refresh Token

**Función**: `create_refresh_token(subject: str)`

**Parámetros de construcción**:
- `sub`: UUID del usuario (string)
- `exp`: Timestamp de expiración (7 días por defecto)
- `type`: Siempre `"refresh"`

**Payload resultante**:
```json
{
  "sub": "9f5008c0-4c39-4da3-a3a6-c9a63a261296",
  "exp": 1736271600,
  "type": "refresh"
}
```

### PASETO Token

**Función**: `create_app_token(user_id: UUID, app_name: str = "gac", expires_in_minutes: int = 5)`

**Parámetros de construcción**:
- `user_id`: UUID del usuario (UUID)
- `app_name`: Nombre de la aplicación (default: "gac")
- `expires_in_minutes`: Minutos de vigencia (default: 5)

**Payload resultante** (compatible con otros servicios):
```json
{
  "internal_id": "9f5008c0-4c39-4da3-a3a6-c9a63a261296",
  "service": "gac",
  "role": "GAC_ADMIN",
  "scope": "internal-gac-admin",
  "iat": "2025-12-08T10:00:00+00:00",
  "exp": "2025-12-08T10:05:00+00:00"
}
```

**Validación en otros servicios**:
```python
# Función compatible: decode_service_token()
payload = decode_service_token(token, required_service="gac", required_role="GAC_ADMIN")
# Retorna el payload si es válido, None si es inválido/expirado
```

---

## 🎯 Casos de Uso

### Caso 1: Usuario Regular
1. **Login** → POST `/auth/login` → Obtiene JWT
2. **Usar API** → Cualquier endpoint con JWT Access
3. **Refresh** → POST `/auth/refresh` → Nuevos tokens JWT

### Caso 2: Administrador
1. **Login** → POST `/auth/login` → Obtiene JWT
2. **Gestión de usuarios** → Endpoints `/users/*` con JWT
3. **Generar PASETO** → POST `/internal/tokens/app` → Token PASETO
4. **Comunicación inter-servicios** → Usar PASETO en otros servicios

### Caso 3: Servicio Externo
1. **Recibir PASETO** → De aplicación GAC
2. **Validar PASETO** → Usar clave compartida PASETO_SECRET_KEY
3. **Extraer información** → internal_id, service, role, scope

---

## 🔐 Configuración Requerida

### Variables de Entorno (.env)

```bash
# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=30
REFRESH_TOKEN_EXPIRES_DAYS=7

# PASETO Configuration
PASETO_SECRET_KEY=your-32-byte-paseto-secret-key-here-base64-encoded

# Database Schema
DB_SCHEME=gac
```

### Claves Secretas

- **JWT_SECRET**: Clave simétrica para JWT (mínimo 32 caracteres)
- **PASETO_SECRET_KEY**: Clave de 32 bytes codificada en base64 para PASETO
- **DB_SCHEME**: Esquema de base de datos (default: "public")

---

## ⚠️ Consideraciones de Seguridad

- **JWT**: Usado para autenticación de usuarios, expira rápidamente
- **PASETO**: Usado para comunicación inter-servicios, expira en 5 minutos
- **Nunca compartir PASETO_SECRET_KEY** entre diferentes entornos
- **Rotar JWT_SECRET** periódicamente
- **Usar HTTPS** en producción

---

## 📊 Resumen por Tipo de Endpoint

| Tipo de Endpoint | Cantidad | Token Requerido | Rol Requerido |
|------------------|----------|-----------------|---------------|
| Públicos | 1 | Ninguno | - |
| JWT Básico | 11 | JWT Access | Usuario autenticado |
| JWT Admin | 11 | JWT Access | `admin` |
| Generadores PASETO | 3 | JWT Access | `admin` |
| **TOTAL** | **26** | - | - |
