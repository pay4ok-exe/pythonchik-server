from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pythonchick API"
    
    # Security
    SECRET_KEY: str = "your-secret-key-for-development"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database - Update with your actual MSSQL connection string
    DATABASE_URL: str = "mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()