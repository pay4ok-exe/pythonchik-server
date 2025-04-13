# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pythonchick API"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Frontend URL for redirects
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://pythonchik-ui.vercel.app")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "u-know-who-am-i")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Database - Using MySQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://pythonchick:pythonchick@localhost:3306/pythonchick"
    )
    
    # Email settings
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "no-reply@pythonchick.com")
    FROM_NAME: str = os.getenv("FROM_NAME", "Pythonchick")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()