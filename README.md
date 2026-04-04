# FactoryFlow ERP — Backend API

Manufacturing ERP system built with **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0**, **Alembic**, and **Docker**.

## Features

- 🔐 **JWT Authentication** — Access + refresh tokens with DB-persisted revocation
- 📦 **Inventory Management** — Dual-unit tracking with weighted average cost (CPP)
- 🏭 **Production Orders** — BOM-based material deduction with ACID transactions
- 🛒 **Sales & Clients** — Sales tracking with client management
- 📊 **Products & BOM** — Product catalog with bill of materials

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Database  | PostgreSQL 16 (Supabase-compatible) |
| ORM       | SQLAlchemy 2.0 |
| Migrations| Alembic |
| Auth      | JWT (python-jose) + bcrypt |
| Container | Docker + Docker Compose |

## Quick Start

### With Docker (recommended)

```bash
docker-compose up --build -d
# Run seed (creates admin user + sample data)
docker-compose exec backend python seed.py
```

### Without Docker

```bash
# Create .env from example
cp .env.example .env
# Edit DATABASE_URL to point to your PostgreSQL instance

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed database
python seed.py

# Start server
uvicorn app.main:app --reload
```

## API Docs

Once running, visit: **http://localhost:8000/docs** (Swagger UI)

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin    | admin123 | admin |

## Project Structure

```
app/
├── main.py                  # FastAPI application + router wiring
├── core/
│   ├── config.py            # Settings from .env
│   ├── security.py          # JWT + bcrypt utilities
│   └── dependencies.py      # get_db, get_current_user
├── db/
│   ├── base.py              # SQLAlchemy DeclarativeBase
│   └── session.py           # Engine + SessionLocal
└── modules/
    ├── auth/                # Register, login, refresh, revoke
    ├── materials/           # Raw materials + units
    ├── inventory/           # Stock movements + CPP calculation
    ├── products/            # Products + BOM
    ├── production/          # Production orders + consumptions
    └── sales/               # Clients + sales
```

## 🔐 Seguridad y Variables de Entorno

El proyecto utiliza un archivo `.env` para gestionar credenciales. **Nunca subas tu archivo `.env` real al repositorio.**

| Variable | Descripción | Recomendación |
|----------|-------------|---------------|
| `POSTGRES_USER` | Usuario de la DB | No usar `postgres` en prod |
| `POSTGRES_PASSWORD` | Contraseña de la DB | Usar una cadena larga y compleja |
| `DATABASE_URL` | URL de conexión SQL | Se construye automáticamente en Docker |
| `SECRET_KEY` | Firma de Access Tokens | Generar con `openssl rand -hex 32` |
| `REFRESH_SECRET_KEY` | Firma de Refresh Tokens | Usar una llave distinta a la anterior |
| `ALGORITHM` | Algoritmo JWT | Por defecto: `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración Access Token | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Duración Refresh Token | `7` |


---

## 🚀 Guía de Prueba Rápida

Si acabas de descargar el proyecto y quieres probarlo de inmediato, sigue este flujo:

### 1. Levantar la infraestructura
Asegúrate de tener Docker instalado y ejecuta:
```bash
docker-compose up --build -d
```
*Este comando levantará la base de datos PostgreSQL y la API de FastAPI automáticamente.*

### 2. Poblar la base de datos (Seed)
Ejecuta el script de semilla para crear el usuario administrador y datos base:
```bash
docker-compose exec backend python seed.py
```

### 3. Probar los Endpoints
1. Abre tu navegador en **[http://localhost:8000/docs](http://localhost:8000/docs)**.
2. Haz clic en el botón **"Authorize"** (icono de candado arriba a la derecha).
3. Ingresa las credenciales: 
   - **Username**: `admin`
   - **Password**: `admin123`
4. Ahora puedes probar cualquier endpoint. Te recomendamos empezar por:
   - `GET /materials/`: Para ver los materiales creados por el seed.
   - `POST /inventory/movements`: Para registrar entradas/salidas de stock.
   - `POST /production-orders/`: Para simular una orden de producción que descuenta materia prima.

### 4. Detener el proyecto
Cuando termines de probar, puedes apagar todo con:
```bash
docker-compose down
```

