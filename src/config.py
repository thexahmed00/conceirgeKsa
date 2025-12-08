from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "mysql+mysql-connector://root:password@localhost:3306/ajla_db"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # App
    debug: bool = True
    log_level: str = "INFO"
    api_version: str = "v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
