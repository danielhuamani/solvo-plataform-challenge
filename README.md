# Solvo Platform API (Django + DRF)

API REST multi-plataforma con autenticación JWT por **plataforma** y un modelo de usuario **no-global** (`PlatformUser`).

## Requisitos

- Python 3.12+
- Docker (opcional, recomendado)

## Setup rápido (Docker)

1. Build

```bash
make build
```

2. Migraciones

```bash
make manage cmd="migrate"
```

3. Seed de plataformas de ejemplo

```bash
make manage cmd="seed_platforms"
```

4. Levantar API

```bash
make up
```

API en:

- `http://localhost:8000/`

Docs:

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

Admin:

- `http://localhost:8000/admin/`

Crear superuser:

```bash
make manage cmd="createsuperuser"
```

## Setup sin Docker

1. Instalar dependencias

```bash
pip install -r src/requirements/base.txt
```

2. Migrar

```bash
python src/manage.py migrate
```

3. Seed plataformas

```bash
python src/manage.py seed_platforms
```

4. Correr server

```bash
python src/manage.py runserver
```

## Variables de entorno

Opcionales:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (default `True`)
- `DJANGO_ALLOWED_HOSTS` (coma-separado)

## Endpoints

Base URL: `/api`

### Auth

- `POST /api/auth/register/`
- `POST /api/auth/login/`

#### Registro

Request:

```json
{
  "platform_slug": "plataforma-a",
  "email": "user@email.com",
  "password": "StrongPass123",
  "first_name": "User",
  "last_name": "Test"
}
```

Response (201):

```json
{
  "id": 1,
  "platform_id": 1,
  "platform_slug": "plataforma-a",
  "email": "user@email.com",
  "first_name": "User",
  "last_name": "Test",
  "is_active": true
}
```

#### Login

Request:

```json
{
  "platform_slug": "plataforma-a",
  "email": "user@email.com",
  "password": "StrongPass123"
}
```

Response (200):

```json
{
  "refresh": "...",
  "access": "..."
}
```

### Devices (protegido)

Header:

`Authorization: Bearer <access_token>`

- `GET /api/devices/` lista los dispositivos del usuario autenticado
- `POST /api/devices/` crea un dispositivo para el usuario autenticado

Create request:

```json
{
  "name": "Macbook",
  "ip_address": "10.0.0.10",
  "is_active": true
}
```

## Tests

Con Docker:

```bash
make manage cmd="test"
```

Sin Docker:

```bash
python src/manage.py test
```

## Linter / Formatter

Se usa **Ruff** para linting y formateo.

Con Docker:

```bash
make lint
make format
```
