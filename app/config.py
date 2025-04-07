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
    
    # Database
    # DATABASE_URL: str = "mssql+pyodbc://@pay4ok/Pythonchick?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    DATABASE_URL: str = "mssql+pyodbc://pay4ok\\pay4ok/Pythonchick?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
print(f"✅ Loaded DATABASE_URL from settings: {settings.DATABASE_URL}")