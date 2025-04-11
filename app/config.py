# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pythonchick API"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "u-know-who-am-i")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Database - Using MySQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://pythonchick:pythonchick@localhost:3306/pythonchick"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()