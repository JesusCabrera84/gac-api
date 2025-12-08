# GAC API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

### Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Body**: `username` (email), `password` (form-data)
- **Response**: Access and refresh tokens.

### Refresh Token
- **URL**: `/auth/refresh`
- **Method**: `POST`
- **Query Param**: `refresh_token`
- **Response**: New access token.

### Get Current User
- **URL**: `/auth/me`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User profile and roles.

## User Management (Admin Only)

### Create User
- **URL**: `/users`
- **Method**: `POST`
- **Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "securepassword",
      "full_name": "John Doe",
      "is_active": true,
      "roles": ["admin", "user"]
    }
    ```
- **Response**: Created user details.

### List Users
- **URL**: `/users`
- **Method**: `GET`
- **Query Params**: `skip` (default 0), `limit` (default 100)
- **Response**: List of users.

### Get User
- **URL**: `/users/{user_id}`
- **Method**: `GET`
- **Response**: User details.

### Update User
- **URL**: `/users/{user_id}`
- **Method**: `PATCH`
- **Body**:
    ```json
    {
      "full_name": "New Name",
      "is_active": false,
      "roles": ["user"]
    }
    ```
- **Response**: Updated user details.

### Delete User (Soft Delete)
- **URL**: `/users/{user_id}`
- **Method**: `DELETE`
- **Response**: Success status.

## Role Management (Admin Only)

### Create Role
- **URL**: `/roles`
- **Method**: `POST`
- **Body**: `{"name": "role_name"}`
- **Response**: Created role.

### List Roles
- **URL**: `/roles`
- **Method**: `GET`
- **Response**: List of all roles.

### Assign Role
- **URL**: `/users/{user_id}/roles/{role_id}`
- **Method**: `POST`
- **Response**: Success status.

### Revoke Role
- **URL**: `/users/{user_id}/roles/{role_id}`
- **Method**: `DELETE`
- **Response**: Success status.

## Business Resources

### Orders
- **Create Order**: `POST /orders`
- **Get Order**: `GET /orders/{order_id}`
- **Get Client Orders**: `GET /clients/{client_id}/orders`

### Payments
- **Create Payment**: `POST /payments`
- **Get Payment**: `GET /payments/{payment_id}`
- **Get Client Payments**: `GET /clients/{client_id}/payments`

### Shipments
- **Create Shipment**: `POST /shipments`
- **Update Status**: `PATCH /shipments/{shipment_id}/status`
- **Get Client Shipments**: `GET /clients/{client_id}/shipments`

### Products
- **List Products**: `GET /products`
- **Create Product**: `POST /products`
    - Body: `{"key": "str", "name": "str", "description": "str"}`

### Devices
- **List Devices**: `GET /devices`
