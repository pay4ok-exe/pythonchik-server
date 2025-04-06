import sys
import os
# Add parent directory to path to import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.course import Course
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.quiz import QuizQuestion, QuizOption
from app.models.user import User
from app.models.progress import UserProgress
from app.utils.database import Base, engine

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()