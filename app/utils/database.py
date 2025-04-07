# app/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create SQLAlchemy engine for MSSQL with Windows Authentication
try:
    # Use the connection string directly
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,  # Set to True for debugging SQL queries
        pool_pre_ping=True
    )
    
    print(f"Database connection established using: {settings.DATABASE_URL}")
except Exception as e:
    print(f"Error setting up database connection: {e}")
    # Fallback to an in-memory SQLite database for testing
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    print("Using fallback SQLite database")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()