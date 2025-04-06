# app/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import urllib.parse

# Parse connection info from URL
params = urllib.parse.quote_plus(f"DRIVER={{{settings.DATABASE_URL.split('?driver=')[1]}}};SERVER={settings.DATABASE_URL.split('//')[1].split('/')[0].split('@')[1]};DATABASE={settings.DATABASE_URL.split('/')[-1].split('?')[0]};UID={settings.DATABASE_URL.split('//')[1].split(':')[0]};PWD={settings.DATABASE_URL.split(':')[2].split('@')[0]}")

# Create SQLAlchemy engine for MSSQL
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,  # Set to True for debugging SQL queries
    pool_pre_ping=True
)

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