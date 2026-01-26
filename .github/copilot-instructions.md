# AJLA Concierge (FastAPI) — Copilot Instructions

## Architecture Overview (Clean Architecture + DDD)
- **Domain layer** (`src/domain/`): Pure business logic. Entities with factory methods (`Request.create(...)`), repository interfaces as `Protocol`, exceptions in `src/domain/shared/exceptions.py`
- **Application layer** (`src/application/`): Use cases with `.execute(...)` method, DTOs (Pydantic models), orchestrates domain objects
- **Infrastructure layer** (`src/infrastructure/`): FastAPI routers, SQLAlchemy models/repos, JWT auth, WebSocket handlers

## Key Data Flows

### Request Submission (Critical Pattern)
`SubmitRequestUseCase.execute(dto, user_id)` atomically creates:
1. `Request` entity → saved via `RequestRepository`
2. `Conversation` linked to request
3. First message from user's description
4. Notifications to all admin users

Example flow: `POST /api/v1/requests` → `requests.py` router → `SubmitRequestUseCase` → repositories

### WebSocket Chat
- Endpoint: `/ws/chat/{conversation_id}?token=<jwt>`
- **Must persist message before broadcasting** — see `ConversationRepository.add_message(...)`
- Broadcast via `ConnectionManager` in `src/infrastructure/web/api/websocket/connection_manager.py`
- Both user and admin clients receive all messages in real-time

## Auth Conventions

### JWT Structure
- User ID in `sub` claim (parsed as `int`)
- Admin flag in `is_admin` claim (checked without DB query)
- Helpers: `get_user_id_from_token()`, `get_token_claims()` in `src/infrastructure/auth/jwt_handler.py`

### Route Protection (use these dependencies)
```python
from src.infrastructure.web.dependencies import get_current_user, get_current_admin_user

# Regular user route
def my_endpoint(user_id: int = Depends(get_current_user)): ...

# Admin-only route
def admin_endpoint(admin_id: int = Depends(get_current_admin_user)): ...
```

## Adding New Features

### New Entity Checklist
1. Domain entity in `src/domain/<feature>/entities/` with factory method and validation
2. Repository interface in `src/domain/<feature>/repository/` as `Protocol`
3. SQLAlchemy model in `src/infrastructure/persistence/models/`
4. Repository impl in `src/infrastructure/persistence/repositories/`
5. DTOs in `src/application/<feature>/dto/`
6. Use case in `src/application/<feature>/use_cases/` with `.execute()` method
7. Dependency factory in `src/infrastructure/web/dependencies/injection.py`
8. Router in `src/infrastructure/web/api/routers/`
9. Register router in `main.py`

### Database Migrations (Alembic)
```bash
# After modifying models in src/infrastructure/persistence/models/
alembic revision --autogenerate -m "Description of change"
alembic upgrade head
```
See `docs/ALEMBIC_GUIDE.md` for detailed workflow.

## Dev Commands
```bash
python main.py                    # Start API (uvicorn with reload if debug=True)
docker-compose up -d              # Start PostgreSQL + pgAdmin
pytest tests/                     # Run tests
alembic upgrade head              # Apply migrations
```

## Exception Handling
Domain exceptions in `src/domain/shared/exceptions.py` are auto-mapped to HTTP responses in `main.py`:
- `ResourceNotFoundError` → 404
- `AccessDeniedError` → 403
- `DuplicateResourceError` → 400
- `DomainException` (fallback) → 400

Throw domain exceptions from use cases; let `main.py` handle the HTTP translation.

## Background Tasks
Scheduler in `src/infrastructure/tasks/scheduler.py` using APScheduler. Runs daily subscription expiration checks. Add new jobs there with `scheduler.add_job(...)`.

## Config
All settings via `src/config.py` (Pydantic `BaseSettings`), loaded from `.env`:
- `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRATION_HOURS`, `DEBUG`
