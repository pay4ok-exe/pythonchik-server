# app/services/topic.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.topic import Topic
from app.models.progress import UserProgress

class TopicService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_topic_with_lessons(self, topic_id, user_id=None):
        try:
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
                    "is_completed": is_completed,
                    "order_index": lesson.order_index
                })
                
            # Determine if the topic should be locked based on previous topics
            is_locked = True
            if not topic.is_locked:
                is_locked = False
            elif user_id:
                # If this is the first topic of the course, it should be unlocked
                if topic.order_index == 0:
                    is_locked = False
                else:
                    # Check the previous topic's completion status
                    previous_topic = self.db.query(Topic).filter(
                        Topic.course_id == topic.course_id,
                        Topic.order_index == topic.order_index - 1
                    ).first()
                    
                    if previous_topic:
                        # Check if all lessons in the previous topic are completed
                        previous_topic_lesson_ids = [l.id for l in previous_topic.lessons]
                        completed_previous_lessons = self.db.query(UserProgress).filter(
                            UserProgress.user_id == user_id,
                            UserProgress.lesson_id.in_(previous_topic_lesson_ids),
                            UserProgress.is_completed == True
                        ).count()
                        
                        is_locked = completed_previous_lessons < len(previous_topic_lesson_ids)
            
            return {
                "id": topic.id,
                "title": topic.title,
                "description": topic.description,
                "is_locked": is_locked,
                "course_id": topic.course_id,
                "order_index": topic.order_index,
                "lessons": lessons
            }
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Database error in get_topic_with_lessons: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_topic_with_lessons: {str(e)}")
            return None