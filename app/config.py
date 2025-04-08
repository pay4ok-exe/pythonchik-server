# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pythonchick API"
    
    # Security
    SECRET_KEY: str = "u-know-who-am-i"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database - Using SQLite for simplicity
    DATABASE_URL: str = "sqlite:///./pythonchick.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
