# Hostel Management System (HMS)

Full-stack Hostel Management System — FastAPI + PostgreSQL + React.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic, JWT
- **Frontend:** React, TypeScript, React Router, Tailwind CSS, React Hook Form, Zod
- **Auth:** Role-based access control (Admin, Staff, Student)

## Features

- JWT authentication with role-based authorization
- Admin dashboard — manage students, room applications, rooms, and notices
- Staff dashboard
- Student dashboard — view room allocation and payments
- RESTful API with auto-generated Swagger docs

## Project Structure

```
HMS/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Route handlers
│   │   ├── core/               # Config, DB, dependencies
│   │   ├── models/             # SQLAlchemy models
│   │   ├── repositories/       # Data access layer
│   │   ├── schemas/            # Pydantic schemas
│   │   └── services/           # Business logic
│   ├── alembic/                # Migrations
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   └── seed.py
└── frontend/
    └── src/
        ├── api/                # API client
        ├── components/         # Shared components
        ├── context/            # Auth state
        ├── layouts/            # App layout
        ├── pages/              # Page components
        ├── routes/             # Route definitions
        └── schemas/            # Zod validation
```

## Requirements

| Tool | Version |
|------|---------|
| Python | 3.11+ |
| Node.js | 20+ |
| PostgreSQL | 16+ |
| Git | Latest |

## Setup

### 1. Create Database

```powershell
psql -U postgres
CREATE DATABASE hms;
\q
```

### 2. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` — set your PostgreSQL password in `DATABASE_URL`:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/hms
```

Then run migrations, seed data, and start:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe seed.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

Open a new terminal:

```powershell
cd frontend
npm install
npm run dev
```

## Run

| App | URL |
|-----|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

## Credentials (DEV ONLY)

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | Admin@123456 |
| Staff | staff | Staff@123456 |
| Student | student | Student@123456 |

## Tests

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ -v
```
