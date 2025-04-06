from sqlalchemy.orm import Session
from app.models.topic import Topic
from app.models.progress import UserProgress

class TopicService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_topic_with_lessons(self, topic_id, user_id=None):
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        
        if not topic:
            return None
            
        # Format response
        lessons = []
        for lesson in topic.lessons:
            # Check if lesson is completed
            is_completed = False
            if user_id:
                progress = self.db.query(UserProgress).filter(
                    UserProgress.user_id == user_id,
                    UserProgress.lesson_id == lesson.id
                ).first()
                
                if progress and progress.is_completed:
                    is_completed = True
            
            lessons.append({
                "id": lesson.id,
                "title": lesson.title,
                "type": lesson.type,
                "is_completed": is_completed
            })
            
        return {
            "id": topic.id,
            "title": topic.title,
            "description": topic.description,
            "is_locked": topic.is_locked,
            "course_id": topic.course_id,
            "lessons": lessons
        }