# scripts/init_db.py
import sys
import os
import pyodbc
import urllib.parse
from sqlalchemy import inspect

# Add parent directory to path to import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.course import Course
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.quiz import QuizQuestion, QuizOption
from app.models.user import User
from app.models.progress import UserProgress
from app.models.achievement import Achievement, UserAchievement
from app.models.activity import UserActivity
from app.utils.database import Base, engine, settings

def init_db():
    # Check if database exists
    try:
        conn_str = settings.DATABASE_URL.replace('+pyodbc', '')
        server = conn_str.split('@')[1].split('/')[0]
        database = conn_str.split('/')[-1].split('?')[0]
        username = conn_str.split('//')[1].split(':')[0]
        password = conn_str.split(':')[2].split('@')[0]
        driver = conn_str.split('driver=')[1]
        
        # Connect to master database to check if our DB exists
        master_conn = pyodbc.connect(f'DRIVER={{{driver}}};SERVER={server};DATABASE=master;UID={username};PWD={password}')
        cursor = master_conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT name FROM sys.databases WHERE name = N'{database}'")
        result = cursor.fetchone()
        
        if not result:
            print(f"Database '{database}' does not exist. Creating...")
            cursor.execute(f"CREATE DATABASE {database}")
            master_conn.commit()
            print(f"Database '{database}' created successfully.")
        else:
            print(f"Database '{database}' already exists.")
            
        cursor.close()
        master_conn.close()
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        return
    
    # Create tables in our database
    try:
        # Get existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        # Create all tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Print results
        all_tables = set(Base.metadata.tables.keys())
        new_tables = all_tables - set(existing_tables)
        
        if new_tables:
            print(f"Created tables: {', '.join(new_tables)}")
        else:
            print("All tables already exist.")
            
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()