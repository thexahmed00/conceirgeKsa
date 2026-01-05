# AJLA Concierge (FastAPI) — Copilot Instructions

## How this repo is wired
- Entry point is [main.py](main.py): registers routers, adds CORS, and maps domain exceptions to JSON `{"detail": ...}`.
- Layering is consistent:
  - Domain: `src/domain/**` (entities + repository interfaces + `src/domain/shared/exceptions.py`)
  - Application: `src/application/**` (DTOs + use cases with `.execute(...)`)
  - Infrastructure: `src/infrastructure/**` (FastAPI routers, SQLAlchemy models/repos, JWT)

## Runtime + config
- Settings live in [src/config.py](src/config.py) and come from `.env` / env vars (`DATABASE_URL`, `JWT_SECRET_KEY`, etc.).
- DB is SQLAlchemy sync engine in [src/infrastructure/persistence/database.py](src/infrastructure/persistence/database.py) using `NullPool` (helps with WebSocket concurrency).
- On startup, `init_db()` runs `Base.metadata.create_all(...)` (dev convenience). For prod/schema changes prefer Alembic in `alembic/`.

## Auth conventions
- JWT helpers are in [src/infrastructure/auth/jwt_handler.py](src/infrastructure/auth/jwt_handler.py).
- User id is stored in the `sub` claim and parsed as `int`; admin access is via `is_admin` claim.
- FastAPI dependencies are centralized in [src/infrastructure/web/dependencies/injection.py](src/infrastructure/web/dependencies/injection.py):
  - Use `get_current_user` for user routes (HTTP Bearer)
  - Use `get_current_admin_user` for admin-only routes (checks `is_admin` claim)

## API + data flows to preserve
- Requests: [src/infrastructure/web/api/routers/requests.py](src/infrastructure/web/api/routers/requests.py) → `SubmitRequestUseCase.execute(dto, user_id)` creates **request + conversation + first message**.
- Conversations: [src/infrastructure/web/api/routers/conversations.py](src/infrastructure/web/api/routers/conversations.py) exposes history + HTTP message send.
- WebSocket chat: [src/infrastructure/web/api/websocket/chat.py](src/infrastructure/web/api/websocket/chat.py) at `/ws/chat/{conversation_id}?token=...`:
  - Auth via `token` query param
  - Persist message via `ConversationRepository.add_message(...)` **before** broadcasting
  - Broadcast fanout handled by [src/infrastructure/web/api/websocket/connection_manager.py](src/infrastructure/web/api/websocket/connection_manager.py)

## Dev workflows (as implemented)
- Run API: `python main.py` (uses `uvicorn` with `reload=settings.debug`).
- Docker Postgres: see [docker-compose.yml](docker-compose.yml) (service is `transaction-db`; note `setup.sh` references old service names and may be stale).
- Tests: `pytest` (tests live under `tests/`; `pytest` is commented out in `requirements.txt`, so install it if missing).
