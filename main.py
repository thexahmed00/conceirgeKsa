from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.config import settings
from src.shared.logger.config import get_logger
from src.infrastructure.persistence.database import init_db, close_db
from src.infrastructure.web.api.routers import auth
from src.infrastructure.web.api.routers import requests
from src.infrastructure.web.api.routers import conversations
from src.infrastructure.web.api.routers import users
from src.infrastructure.web.api.routers import admin
from src.infrastructure.web.api.websocket import chat

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AJLA Concierge API",
    description="Premium lifestyle concierge platform API",
    version="1.0.0",
)

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
    init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AJLA API shutting down...")
    close_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(requests.router)
app.include_router(conversations.router)
app.include_router(admin.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
