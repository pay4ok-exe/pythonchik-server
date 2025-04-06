from sqlalchemy.orm import Session
from app.models.progress import UserProgress
from app.models.lesson import Lesson
from app.models.user import User
from app.repositories.progress import ProgressRepository
from app.repositories.user import UserRepository
from datetime import datetime, timedelta

class ProgressService:
    def __init__(self, db: Session):
        self.db = db
        self.progress_repository = ProgressRepository(db)
        self.user_repository = UserRepository(db)
    
    def complete_lesson(self, user_id: int, lesson_id: int, score: int = None):
        # Get the lesson to calculate rewards
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            return None
            
        # Create or update progress record
        progress = self.progress_repository.get_by_user_and_lesson(user_id, lesson_id)
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                lesson_id=lesson_id,
                is_completed=True,
                score=score,
                completed_at=datetime.utcnow(),
                attempts=1
            )
            self.db.add(progress)
        else:
            progress.is_completed = True
            progress.score = score if score is not None else progress.score
            progress.completed_at = datetime.utcnow()
            progress.attempts += 1
            progress.updated_at = datetime.utcnow()
        
        # Update user experience and coins
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.experience += lesson.xp_reward
            user.coins += lesson.coins_reward
            
            # Update level based on experience
            user.level = (user.experience // 100) + 1
            
            # Update streak
            last_activity = self.progress_repository.get_last_completed(user_id)
            if last_activity:
                yesterday = datetime.utcnow() - timedelta(days=1)
                if last_activity.completed_at.date() >= yesterday.date():
                    user.streak += 1
                else:
                    user.streak = 1
            else:
                user.streak = 1
        
        self.db.commit()
        
        return progress