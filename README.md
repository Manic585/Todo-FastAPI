# FastAPI Todos App

A full-stack Todo application built with FastAPI, SQLAlchemy, Jinja2 templates, and JWT authentication. This project was built as a learning exercise covering core FastAPI concepts from basic routing through database integration, authentication, and testing.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [UI Pages](#ui-pages)
- [Authentication](#authentication)
- [Running the App](#running-the-app)
- [Running Tests](#running-tests)
- [Database Migrations](#database-migrations)
- [Learning Modules](#learning-modules)

---

## Project Structure

```
fastapi/
├── main.py                  # App entry point, router registration, static files
├── database.py              # SQLAlchemy engine and session setup
├── models.py                # ORM models (Users, Todos)
├── alembic.ini              # Alembic configuration
├── alembic/
│   └── versions/            # Migration scripts
│       └── aeff25f89db0_create_phone_number_for_user_col.py
├── routers/
│   ├── auth.py              # Registration, login, JWT token generation
│   ├── todos.py             # CRUD operations for todos
│   ├── admin.py             # Admin-only endpoints
│   └── users.py             # User profile and password management
├── templates/               # Jinja2 HTML templates
│   ├── layout.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── todo-page.html
│   └── edit-todo.html
├── static/
│   ├── css/                 # Bootstrap + custom styles
│   └── js/                  # Bootstrap + jQuery
├── test/
│   ├── utils.py             # Shared fixtures and test DB setup
│   ├── test_auth.py
│   ├── test_todos.py
│   ├── test_admin.py
│   ├── test_users.py
│   └── test_main.py
├── books.py                 # Learning module: basic routing with in-memory data
└── books2.py                # Learning module: Pydantic models, Path/Query params
```

---

## Features

- User registration and login with bcrypt-hashed passwords
- JWT-based authentication (Bearer tokens + cookie-based for UI)
- Todo CRUD with ownership enforcement (users only see their own todos)
- Admin role with read-all and delete-any-todo privileges
- User profile endpoints: view info, change password, update phone number
- Server-side rendered UI using Jinja2 + Bootstrap
- Database migrations with Alembic
- Full test suite with an isolated SQLite test database

---

## Tech Stack

| Layer         | Technology                              |
|---------------|-----------------------------------------|
| Framework     | FastAPI                                 |
| ORM           | SQLAlchemy                              |
| Database      | SQLite (`todosapp.db`)                  |
| Migrations    | Alembic                                 |
| Auth          | JWT (`python-jose`), bcrypt (`passlib`) |
| Templating    | Jinja2                                  |
| Frontend      | Bootstrap 4, jQuery                     |
| Testing       | pytest, FastAPI TestClient              |
| Python        | 3.14                                    |

---

## Database Schema

### `users`

| Column            | Type    | Notes                     |
|-------------------|---------|---------------------------|
| `id`              | Integer | Primary key               |
| `email`           | String  | Unique                    |
| `username`        | String  | Unique                    |
| `first_name`      | String  |                           |
| `last_name`       | String  |                           |
| `hashed_password` | String  | bcrypt hash               |
| `is_active`       | Boolean | Default `true`            |
| `role`            | String  | `"admin"` or `"user"`     |
| `phone_number`    | String  | Added via Alembic migration |

### `todos`

| Column       | Type    | Notes                        |
|--------------|---------|------------------------------|
| `id`         | Integer | Primary key                  |
| `title`      | String  |                              |
| `description`| String  |                              |
| `priority`   | Integer | 1–5                          |
| `complete`   | Boolean | Default `false`              |
| `owner_id`   | Integer | FK → `users.id`              |

---

## API Reference

### Health

| Method | Path       | Description              |
|--------|------------|--------------------------|
| GET    | `/healthy` | Health check             |

### Auth — `/auth`

| Method | Path             | Description                                    | Auth |
|--------|------------------|------------------------------------------------|------|
| POST   | `/auth/`         | Register a new user                            | No   |
| POST   | `/auth/token`    | Login and receive a JWT access token           | No   |
| GET    | `/auth/login-page`    | Render the login HTML page                | No   |
| GET    | `/auth/register-page` | Render the register HTML page             | No   |

**Register request body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "firstname": "John",
  "last_name": "Doe",
  "password": "secret123",
  "role": "user",
  "phone_number": "555-1234"
}
```

**Token response:**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

---

### Todos — `/todos`

All API endpoints require a valid JWT bearer token. The UI routes use a cookie instead.

| Method | Path                          | Description                    |
|--------|-------------------------------|--------------------------------|
| GET    | `/todos/`                     | List all todos for current user |
| GET    | `/todos/todo/{id}`            | Get a single todo by ID        |
| POST   | `/todos/todo`                 | Create a new todo              |
| PUT    | `/todos/todo/{id}`            | Update a todo                  |
| DELETE | `/todos/todo/{id}`            | Delete a todo                  |
| GET    | `/todos/todo-page`            | Render the todos UI page       |
| GET    | `/todos/edit-todo-page/{id}`  | Render the edit-todo UI page   |

**Todo request body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": 3,
  "complete": false
}
```

Validation rules: `title` min 3 chars, `description` 3–100 chars, `priority` 1–5.

---

### Admin — `/admin`

Requires JWT with `role: "admin"`.

| Method | Path                  | Description              |
|--------|-----------------------|--------------------------|
| GET    | `/admin/todo`         | List all todos (all users) |
| DELETE | `/admin/todo/{id}`    | Delete any todo by ID    |

---

### Users — `/user`

Requires JWT bearer token.

| Method | Path                          | Description                  |
|--------|-------------------------------|------------------------------|
| GET    | `/user/`                      | Get current user's profile   |
| PUT    | `/user/password`              | Change password              |
| PUT    | `/user/phonenumber/{number}`  | Update phone number          |

**Change password request body:**
```json
{
  "password": "currentpassword",
  "new_password": "newsecurepassword"
}
```

---

## UI Pages

| Route                       | Description                                |
|-----------------------------|--------------------------------------------|
| `/`                         | Home page                                  |
| `/auth/login-page`          | Login form                                 |
| `/auth/register-page`       | Registration form                          |
| `/todos/todo-page`          | View all todos (redirects to login if not authenticated) |
| `/todos/edit-todo-page/{id}`| Edit a specific todo                       |

The UI reads the JWT from a cookie (`access_token`) set after login.

---

## Authentication

Tokens are signed with HS256 and expire after **20 minutes**.

**JWT payload:**
```json
{
  "sub": "username",
  "id": 1,
  "role": "user",
  "exp": 1234567890
}
```

For API access, pass the token in the `Authorization` header:
```
Authorization: Bearer <token>
```

For UI access, the token is stored in a browser cookie and decoded on each request.

---

## Running the App

### 1. Set up the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy passlib python-jose jinja2 python-multipart alembic
```

### 2. Start the development server

```bash
uvicorn main:app --reload
```

The app will be available at `http://localhost:8000`.

Interactive API docs: `http://localhost:8000/docs`

---

## Running Tests

Tests use an isolated in-memory SQLite database and override the `get_db` and `get_current_user` dependencies.

```bash
pytest test/ -v
```

Test files:

| File              | Coverage                                      |
|-------------------|-----------------------------------------------|
| `test_auth.py`    | User authentication, token creation/decoding  |
| `test_todos.py`   | Todo CRUD (create, read, update, delete)      |
| `test_admin.py`   | Admin read-all and delete endpoints           |
| `test_users.py`   | Profile retrieval, password and phone updates |
| `test_main.py`    | Root endpoint and health check                |

---

## Database Migrations

Migrations are managed with Alembic.

**Apply all migrations:**
```bash
alembic upgrade head
```

**Create a new migration:**
```bash
alembic revision --autogenerate -m "description of change"
```

**Roll back one migration:**
```bash
alembic downgrade -1
```

Current migrations:
- `aeff25f89db0` — Added `phone_number` column to the `users` table

---

## Learning Modules

Two standalone scripts demonstrate foundational FastAPI concepts:

### `books.py` — Basic Routing

Covers path parameters, query parameters, request body with `Body()`, and in-memory CRUD with a plain list. Run with:
```bash
uvicorn books:app --reload
```

### `books2.py` — Pydantic Models & Validation

Introduces `BaseModel`, `Field` validation, `Path`/`Query` parameters with constraints, `HTTPException` with status codes, and auto-incrementing IDs. Run with:
```bash
uvicorn books2:app --reload
```
