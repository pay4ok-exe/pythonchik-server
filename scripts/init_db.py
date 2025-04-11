# scripts/init_db.py
import sys
import os
from pathlib import Path

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
from app.models.challenge import CodingChallenge, UserChallenge
from app.utils.database import Base, engine
from app.config import settings

def init_db():
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Create migrations directory if it doesn't exist
        migrations_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "migrations" / "versions"
        migrations_dir.mkdir(parents=True, exist_ok=True)
        
        print("You can now run 'alembic revision --autogenerate -m \"initial\"' to create migration files")
        print("Then run 'alembic upgrade head' to apply migrations")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("Please ensure the database exists and the connection settings are correct.")
        print(f"Current database URL: {settings.DATABASE_URL}")

if __name__ == "__main__":
    init_db()