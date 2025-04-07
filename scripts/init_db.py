# scripts/init_db.py
import sys
import os
import pyodbc
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
    try:
        # First verify connection using pyodbc directly
        conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Pythonchick;Trusted_Connection=yes;"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME")
        row = cursor.fetchone()
        print(f"Direct connection successful to server: {row[0]}")
        conn.close()
        
        # Now use SQLAlchemy to create tables
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        print("✅ Tables in DB:")
        for table_name in inspector.get_table_names():
            print(f" - {table_name}")

        print("Database tables created successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        print("Please ensure the database exists and your Windows user has appropriate permissions.")

if __name__ == "__main__":
    init_db()