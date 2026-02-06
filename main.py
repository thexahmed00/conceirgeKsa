from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from src.config import settings
from src.shared.logger.config import get_logger
from src.infrastructure.persistence.database import init_db, close_db
from src.infrastructure.tasks import start_scheduler, stop_scheduler
from src.infrastructure.web.api.routers import auth
from src.infrastructure.web.api.routers import requests
from src.infrastructure.web.api.routers import conversations
from src.infrastructure.web.api.routers import users
from src.infrastructure.web.api.routers import admin
from src.infrastructure.web.api.routers import admin_users
from src.infrastructure.web.api.routers import websocket_docs
from src.infrastructure.web.api.routers import services
from src.infrastructure.web.api.routers import admin_services
from src.infrastructure.web.api.routers import bookings
from src.infrastructure.web.api.routers import plans
from src.infrastructure.web.api.routers import notifications
from src.infrastructure.web.api.routers import content
from src.infrastructure.web.api.routers import admin_plans
from src.infrastructure.web.api.routers import admin_tasks
from src.infrastructure.web.api.websocket import chat
from src.domain.shared.exceptions import (
    AccessDeniedError,
    DomainException,
    DuplicateResourceError,
    InvalidUserError,
    ResourceNotFoundError,
)

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AJLA Concierge API",
    description="Premium lifestyle concierge platform API",
    version="1.0.0",
)


@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(_: Request, exc: ResourceNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AccessDeniedError)
async def access_denied_handler(_: Request, exc: AccessDeniedError):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.exception_handler(DuplicateResourceError)
async def duplicate_resource_handler(_: Request, exc: DuplicateResourceError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(InvalidUserError)
async def invalid_user_handler(_: Request, exc: InvalidUserError):
    # Used by registration flow; login still custom-handled for WWW-Authenticate header.
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(DomainException)
async def domain_exception_handler(_: Request, exc: DomainException):
    # Fallback for domain validation errors (InvalidRequestError, InvalidMessageError, etc.)
    return JSONResponse(status_code=400, content={"detail": str(exc)})

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("AJLA API starting up...")
    # Database schema is managed by Alembic migrations (run before app startup in Docker/EC2)
    # init_db() is no longer called—migrations ensure schema is up-to-date
    logger.info("Database ready (migrations applied)")
    
    # Start background scheduler for periodic tasks
    start_scheduler()
    logger.info("Background scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AJLA API shutting down...")
    
    # Stop background scheduler
    stop_scheduler()
    
    # Close database connections
    close_db()

@app.get("/")
async def root():
    return {"message": "Welcome to AJLA Concierge API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(requests.router)
app.include_router(conversations.router)
app.include_router(admin.router)
app.include_router(admin_users.router)
app.include_router(services.router)
app.include_router(admin_services.router)
app.include_router(websocket_docs.router)  # WebSocket documentation endpoint
app.include_router(chat.router)  # WebSocket endpoint (won't show in Swagger)
app.include_router(bookings.router)
app.include_router(plans.router)
app.include_router(notifications.router)
app.include_router(content.router)
app.include_router(admin_plans.router)
app.include_router(admin_tasks.router)

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
