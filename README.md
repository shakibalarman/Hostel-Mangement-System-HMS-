# Hostel Management System (HMS)

A full-stack, production-style Hostel Management System built with FastAPI, PostgreSQL, React, and TypeScript.

## Tech Stack

**Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic, PostgreSQL, JWT, bcrypt

**Frontend:** React 19, TypeScript, Vite, Tailwind CSS 4, React Router, Axios, TanStack React Query, React Hook Form, Zod

**Database:** PostgreSQL 16

## Features

- **Authentication & Authorization:** JWT-based auth with role-based access control (ADMIN, STAFF, STUDENT)
- **Hostel Management:** Manage hostels, buildings, floors, rooms, and beds
- **Student Management:** Student registration, profiles, and allocation
- **Room Allocation:** Apply, approve, allocate beds, transfer, and checkout
- **Fee Management:** Fee structures, payments, and expense tracking
- **Attendance:** Mark and track student attendance
- **Leave Management:** Submit and approve leave requests
- **Complaints & Maintenance:** Submit and track complaints and maintenance requests
- **Meals & Inventory:** Manage meal schedules and inventory items
- **Notices & Notifications:** Publish notices and send notifications
- **Reports:** Dashboard statistics, occupancy reports, payment reports

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── core/                # Config, database, security, dependencies
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── api/v1/endpoints/    # API route handlers
│   │   ├── services/            # Business logic layer
│   │   ├── repositories/        # Data access layer
│   │   └── utils/               # Utility functions
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Pytest test suite
│   ├── seed.py                  # Development seed script
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── layouts/             # App layout with sidebar
│   │   ├── pages/               # Page components (admin/staff/student)
│   │   ├── routes/              # React Router configuration
│   │   ├── api/                 # Axios API clients
│   │   ├── context/             # React context providers
│   │   ├── types/               # TypeScript type definitions
│   │   └── schemas/             # Zod validation schemas
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+

### Backend Setup

1. Create a virtual environment and install dependencies:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure environment variables:
```powershell
copy .env.example .env
# Edit .env with your database credentials
```

3. Run database migrations:
```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

4. Seed development data:
```powershell
.\.venv\Scripts\python.exe seed.py
```

5. Start the development server:
```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

API documentation will be available at `http://localhost:8000/docs`

### Frontend Setup

1. Install dependencies:
```powershell
cd frontend
npm install
```

2. Start the development server:
```powershell
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Development Credentials

> **WARNING:** These are DEVELOPMENT ONLY credentials. Do not use in production.

| Role    | Username | Password      |
|---------|----------|---------------|
| Admin   | admin    | Admin@123456  |
| Staff   | staff    | Staff@123456  |
| Student | student  | Student@123456|

## Running Tests

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

## API Endpoints

All endpoints are prefixed with `/api/v1/`.

- `/auth` - Authentication (login, logout, me)
- `/hostels` - Hostel management
- `/buildings` - Building management
- `/floors` - Floor management
- `/rooms` - Room management
- `/beds` - Bed management
- `/students` - Student management
- `/staff` - Staff management
- `/users` - User management
- `/applications` - Hostel applications
- `/allocations` - Room allocations
- `/fees` - Fee structures
- `/payments` - Payments
- `/expenses` - Expenses
- `/attendance` - Attendance records
- `/leaves` - Leave requests
- `/complaints` - Complaints
- `/maintenance` - Maintenance requests
- `/meals` - Meal management
- `/inventory` - Inventory management
- `/notices` - Notices
- `/notifications` - User notifications
- `/reports` - Reports and dashboard stats

## License

MIT
