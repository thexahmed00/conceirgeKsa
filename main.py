from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from src.config import settings
from src.shared.logger.config import get_logger
from src.infrastructure.persistence.database import init_db, close_db
from src.infrastructure.web.api.routers import auth
from src.infrastructure.web.api.routers import requests
from src.infrastructure.web.api.routers import conversations
from src.infrastructure.web.api.routers import users
from src.infrastructure.web.api.routers import admin
from src.infrastructure.web.api.routers import websocket_docs
from src.infrastructure.web.api.routers import services
from src.infrastructure.web.api.routers import admin_services
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
    # init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AJLA API shutting down...")
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
app.include_router(services.router)
app.include_router(admin_services.router)
app.include_router(websocket_docs.router)  # WebSocket documentation endpoint
app.include_router(chat.router)  # WebSocket endpoint (won't show in Swagger)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
