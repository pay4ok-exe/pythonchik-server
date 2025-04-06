# app/repositories/progress.py
from sqlalchemy.orm import Session
from app.models.progress import UserProgress
from datetime import datetime

class ProgressRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_user_and_lesson(self, user_id: int, lesson_id: int):
        return self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id == lesson_id
        ).first()
    
    def get_last_completed(self, user_id: int):
        return self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.is_completed == True
        ).order_by(UserProgress.completed_at.desc()).first()