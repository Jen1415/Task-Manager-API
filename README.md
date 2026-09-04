# Task Manager API

A REST API for managing personal tasks, built with FastAPI and PostgreSQL. Supports user registration, JWT-based authentication, and full CRUD on tasks scoped to the authenticated user.

**Live demo:** `https://task-manger-api.onrender.com/docs` *(replace with your actual Render URL)*

---

## Features

- User registration with hashed passwords (bcrypt via passlib)
- JWT-based login (OAuth2 password flow)
- Full CRUD on tasks: create, list (paginated), retrieve, update, delete
- Ownership isolation — users can only see and modify their own tasks (cross-user access returns `404`, not `403`, to avoid leaking resource existence)
- Fully tested with pytest + httpx (async, in-process ASGI client)
- Containerized with Docker; deployed on Render

---

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM / Migrations:** SQLAlchemy + Alembic
- **Auth:** python-jose (JWT, HS256), passlib/bcrypt (password hashing)
- **Testing:** pytest, httpx, pytest-asyncio
- **Package management:** [`uv`](https://docs.astral.sh/uv/)
- **Containerization:** Docker + Docker Compose
- **Deployment:** Render (Web Service + managed PostgreSQL)

---

## Architecture Notes

- **`src/` layout:** the application package lives at `src/taskmanagerapi/`, with `tests/` at the repo root.
- **Layering convention:**
  - `routers/` — HTTP concerns only (status codes, `HTTPException`, request/response schemas)
  - `crud/` — pure DB logic, no HTTP awareness; returns `None`/`[]` when not found, never raises `HTTPException`
  - `core/` — auth internals (JWT creation/decoding, password hashing context, `get_current_user` dependency)
- **Schemas never mirror DB models 1:1** — e.g. `UserCreate` accepts a plaintext `password` but `UserResponse` never returns `hashed_password`; `TaskCreate` never accepts `owner_id` from the client (it's set server-side from the authenticated user).
- **Ownership-scoped queries filter in the query itself** (not fetch-then-check), and return `404` for another user's resource rather than `403`, so as not to reveal that the resource exists at all.

---

## Local Development

### Option A — Docker Compose (recommended, matches production)

```bash
docker compose up --build
```

This starts both the API and a Postgres container. The API will be available at `http://localhost:8000`.

### Option B — Native (uv + local Postgres)

Requires a running local PostgreSQL instance.

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn taskmanagerapi.main:app --reload
```

> Run all commands from the repo root — `.env` loading and imports depend on it.

---

## Environment Variables

Create a `.env` file in the repo root (see `.env.example`):

| Variable       | Description                                      |
|----------------|---------------------------------------------------|
| `DATABASE_URL` | PostgreSQL connection string                       |
| `JWT_SECRET`   | Secret key used to sign JWTs — no default; the app will fail to start if this is missing |

For running tests, a separate `.env.test` points `DATABASE_URL` at a dedicated test database.

---

## Running Tests

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov=taskmanagerapi --cov-report=term-missing
```

Tests use a real (rolled-back) database transaction per test for isolation, and cover registration, login, protected-route access, full task CRUD, and cross-user ownership isolation.

---

## API Documentation

Once running, interactive API docs (Swagger UI) are available at:

```
https://task-manager-api-pbj8.onrender.com/docs
```

> **Note:** Swagger UI does not automatically attach a token from `/auth/login` to subsequent requests. After logging in, copy the `access_token` and paste it into the **Authorize** dialog (lock icon) to test protected endpoints.

---

## Deployment

Deployed on [Render](https://render.com) as a Docker-based Web Service, with a managed Render PostgreSQL instance. Environment variables (`DATABASE_URL`, `JWT_SECRET`) are configured in the Render dashboard, not committed to the repo.

---

## Project Status

Core CRUD, auth, testing, containerization, and deployment are complete. Not yet implemented: refresh tokens, rate limiting on auth endpoints, structured logging (see stretch goals).