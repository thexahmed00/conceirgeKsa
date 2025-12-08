from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.config import settings
from src.shared.logger.config import get_logger

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

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AJLA API shutting down...")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# TODO: Import and include routers
# from src.infrastructure.web.api.routers import auth, users, requests, conversations

# app.include_router(auth.router, prefix="/api/v1/auth")
# app.include_router(users.router, prefix="/api/v1/users")
# app.include_router(requests.router, prefix="/api/v1/requests")
# app.include_router(conversations.router, prefix="/api/v1/conversations")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
