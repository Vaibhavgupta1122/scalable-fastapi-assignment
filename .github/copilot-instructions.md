# Copilot Instructions for Scalable FastAPI + React Assignment

This is a full-stack authentication and role-based task management system: **FastAPI backend** + **React (TypeScript) frontend**.

## Quick Start

### Commands

**Backend**
```bash
# Terminal: python | cd backend
pip install -r requirements.txt
python init_db.py                    # Create tables & default admin user
python create_demo_data.py           # Seed demo data (4 users, multiple tasks)
uvicorn app.main:app --reload        # Start API on http://localhost:8000
```

**Frontend**
```bash
# Terminal: powershell | cd frontend
npm install
npm start                             # Start dev server on http://localhost:3000
```

**All-in-one**: Run `start_all.bat` from workspace root (Windows only).

### Database Credentials (Dev)
- **Default Admin**: admin@example.com / admin123
- **Demo Users**: john@demo.com, jane@demo.com, bob@demo.com (all password: "password")
- **Default DB**: PostgreSQL at `postgresql://user:password@localhost/dbname` (see backend/.env or [config.py](backend/app/core/config.py))

---

## Architecture

### Backend: FastAPI (Port 8000)

**Structure**: [backend/app](backend/app)
```
core/          Config, JWT security, CORS
db/            SQLAlchemy setup
models/        ORM models (User, Task)
schemas/       Pydantic request/response models
routers/       API endpoints (/auth, /tasks, /users)
services/      Business logic (auth, user CRUD, task CRUD)
main.py        FastAPI app root
```

**Key Patterns**:
- **Auth**: JWT tokens (HS256, 30-min expiry), role-based access control (USER/ADMIN)
- **DB**: SQLAlchemy 2.0 + PostgreSQL, manual table creation via [init_db.py](backend/init_db.py)
- **Services**: CRUD logic encapsulated in [backend/app/services](backend/app/services), dependencies handle ownership validation
- **Validation**: Pydantic models auto-validate request bodies

**Core Files**:
- [main.py](backend/app/main.py) – FastAPI app setup & root endpoint
- [config.py](backend/app/core/config.py) – Settings (DB URL, JWT secret, CORS origins, API prefix `/api/v1`)
- [security.py](backend/app/core/security.py) – JWT middleware, current_user dependency, role checkers
- [models/user.py](backend/app/models/user.py), [models/task.py](backend/app/models/task.py) – ORM models with enums
- [routers/auth.py](backend/app/routers/auth.py) – Register, login endpoints
- [routers/tasks.py](backend/app/routers/tasks.py) – Task CRUD with ownership checks
- [routers/users.py](backend/app/routers/users.py) – User info (me endpoint), admin user list

### Frontend: React + TypeScript (Port 3000)

**Structure**: [frontend/src](frontend/src)
```
components/    React UI (Login, Dashboard)
contexts/      AuthContext for state management
services/      API clients (axios + interceptor)
types/         TypeScript interfaces (auth, task types)
```

**Key Patterns**:
- **State**: React Context API (see [AuthContext.tsx](frontend/src/contexts/AuthContext.tsx)) with localStorage persistence
- **HTTP**: Axios with interceptor auto-adds Bearer token (see [api.ts](frontend/src/services/api.ts))
- **Routing**: Simple App.tsx conditional render (Login if !authenticated, Dashboard if authenticated)
- **Forms**: Dual-mode login/register in [Login.tsx](frontend/src/components/Login.tsx)

**Core Files**:
- [App.tsx](frontend/src/App.tsx) – Root component, conditional render
- [AuthContext.tsx](frontend/src/contexts/AuthContext.tsx) – Auth state, login/register/logout logic
- [services/api.ts](frontend/src/services/api.ts) – Axios instance with auth token interceptor
- [components/Login.tsx](frontend/src/components/Login.tsx) – Auth UI (dual-mode)
- [components/Dashboard.tsx](frontend/src/components/Dashboard.tsx) – Task CRUD UI
- [types/auth.ts](frontend/src/types/auth.ts) – TypeScript definitions

---

## Development Conventions

| Aspect | Convention | Example |
|--------|-----------|---------|
| **Backend File Names** | snake_case | `user.py`, `create_access_token()` |
| **Backend Classes** | PascalCase | `User`, `Task` |
| **Backend Enums** | UPPER_SNAKE_CASE | `Role.USER`, `TaskStatus.IN_PROGRESS` |
| **Frontend Files** | PascalCase (components), camelCase (services) | `Dashboard.tsx`, `getUser()` |
| **Frontend CSS** | dash-separated, same name as component | `Dashboard.css` |
| **Routing** | RESTful endpoints, `/api/v1` prefix | `GET /api/v1/tasks?skip=0&limit=100` |
| **Pagination** | Query params: `skip`, `limit` | Default: skip=0, limit=100 |
| **Error Handling** | HTTPException with status codes (backend), try-catch (frontend) | `raise HTTPException(status_code=403, detail="Not authorized")` |

---

## Key Architectural Decisions

### Role-Based Access Control
- **Model**: User has `role` field (`USER` or `ADMIN`) and `is_active` flag
- **Enforcement**: 
  - `require_admin()` → only ADMIN can access
  - `require_user_or_admin()` → USER and ADMIN can access
  - Task ownership: non-admin users can only modify their own tasks
- **Files**: [security.py](backend/app/core/security.py) (dependencies), [auth.py](backend/app/routers/auth.py) (enforcement in route decorators)

### Task Ownership Model
- Each task has `owner_id` (FK to User)
- Service layer filters: `get_tasks()` returns owner's tasks for USER, all tasks for ADMIN
- Update logic: `is_completed=True` triggers `status="COMPLETED"` + sets `completed_at` timestamp
- See: [services/task.py](backend/app/services/task.py)

### Database Schema
- **User Model**: id, email (unique), username (unique), hashed_password, full_name, role, is_active, created_at, updated_at
- **Task Model**: id, title, description, status (TODO|IN_PROGRESS|COMPLETED), priority (LOW|MEDIUM|HIGH), is_completed, owner_id (FK), created_at, updated_at, completed_at
- Migrations: Using Alembic (see [alembic.ini](backend/alembic.ini)); manual table creation in [init_db.py](backend/init_db.py) for quick setup

### Frontend State Management
- Single source of truth: React Context with `user`, `isLoading`, `isAuthenticated` state
- Persistence: access token stored in `localStorage['access_token']`
- Auto-refresh on mount to restore session if token exists
- See: [AuthContext.tsx](frontend/src/contexts/AuthContext.tsx)

---

## Common Pitfalls & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Token missing in API calls | Frontend context not initialized | Ensure AuthContext wraps App in index.tsx |
| 403 Forbidden errors | Not passing ownership validation | Check task `owner_id` matches `current_user.id` |
| CORS errors | Frontend/backend ports mismatch | Verify [config.py](backend/app/core/config.py) CORS_ORIGINS includes frontend URL |
| "is_completed" not triggering status | Update logic expects `is_completed=True` in request | See [services/task.py](backend/app/services/task.py) `update_task()` logic |
| Stale token after backend restart | Frontend caches expired token in localStorage | Clear localStorage and re-login, or token refresh logic (not yet implemented) |

---

## Testing

**Frontend**: React Testing Library setup ready (see package.json test scripts)  
**Backend**: pytest compatible; no test suite yet (good area for contributions)

Run frontend tests: `npm test`

---

## Environment & Configuration

### Backend (.env or [config.py](backend/app/core/config.py) defaults)
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (hardcoded in [api.ts](frontend/src/services/api.ts))
```
BASE_URL=http://localhost:8000/api/v1
```

---

## Useful Patterns for AI Assistance

When working on this codebase:

1. **Adding new endpoints**: Follow the pattern in [routers/tasks.py](backend/app/routers/tasks.py):
   - Define Pydantic schema in [schemas/](backend/app/schemas/)
   - Implement service method in [services/](backend/app/services/)
   - Add dependency injection for DB and auth
   - Use `@router.get()` / `@router.post()` decorators

2. **New task properties**: 
   - Add field to [models/task.py](backend/app/models/task.py) ORM model
   - Update Pydantic schemas in [schemas/task.py](backend/app/schemas/task.py)
   - Modify service CRUD in [services/task.py](backend/app/services/task.py)
   - Update frontend types [types/auth.ts](frontend/src/types/auth.ts)
   - Update Dashboard UI [components/Dashboard.tsx](frontend/src/components/Dashboard.tsx)

3. **New API roles**: 
   - Add to User role enum in [models/user.py](backend/app/models/user.py)
   - Create new `require_<role>()` in [security.py](backend/app/core/security.py)
   - Apply decorator to relevant routes

4. **Frontend API calls**:
   - Use Axios instance from [services/api.ts](frontend/src/services/api.ts) (auto-adds auth token)
   - Wrap in try-catch in component or custom hook
   - Set error state and loading state

---

## Links to Key Architecture Examples

- **Full Task CRUD**: [routers/tasks.py](backend/app/routers/tasks.py) – Shows service integration, dependency injection, role checks
- **State persistence**: [AuthContext.tsx](frontend/src/contexts/AuthContext.tsx) – Shows Context API pattern with localStorage
- **API integration**: [services/api.ts](frontend/src/services/api.ts) – Axios interceptor pattern
- **Role-based access**: [security.py](backend/app/core/security.py) – Dependency injection for auth/authorization
- **Database setup**: [database.py](backend/app/db/database.py) + [init_db.py](backend/init_db.py) – SQLAlchemy + manual migration

---

## Quick Reference: Common API Routes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | ✗ | Register new user |
| POST | /auth/login | ✗ | Login (returns JWT token) |
| GET | /users/me | ✓ | Get current user |
| GET | /users?skip=0&limit=100 | ✓ ADMIN | List all users |
| GET | /tasks?skip=0&limit=100 | ✓ | List user's tasks (non-admin) or all (admin) |
| POST | /tasks | ✓ | Create task |
| GET | /tasks/{task_id} | ✓ | Get single task |
| PUT | /tasks/{task_id} | ✓ | Update task |
| DELETE | /tasks/{task_id} | ✓ | Delete task |

---

**Last Updated**: 2026-04-15  
**Project**: Scalable REST API with Authentication & Role-Based Access (Backend Internship Assignment)
