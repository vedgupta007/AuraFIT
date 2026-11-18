from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Resolve the backend directory (two levels up from config.py: app/core/ -> app/ -> backend/)
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "AuraFIT API"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "aurafit"
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Security
    JWT_SECRET_KEY: str = "your_super_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI Provider
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), extra="ignore")

settings = Settings()

