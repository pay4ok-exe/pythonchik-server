from sqlalchemy.orm import Session
from app.models.course import Course
from app.models.topic import Topic
from app.models.progress import UserProgress

class CourseService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_courses(self, user_id=None):
        courses = self.db.query(Course).order_by(Course.order_index).all()
        
        result = []
        for course in courses:
            # Count total topics
            total_topics = len(course.topics)
            
            # Count completed topics (all lessons in topic completed)
            completed_topics = 0
            if user_id:
                for topic in course.topics:
                    # Get all lesson IDs for this topic
                    lesson_ids = [lesson.id for lesson in topic.lessons]
                    if not lesson_ids:
                        continue
                        
                    # Count completed lessons
                    completed_lessons = self.db.query(UserProgress).filter(
                        UserProgress.user_id == user_id,
                        UserProgress.lesson_id.in_(lesson_ids),
                        UserProgress.is_completed == True
                    ).count()
                    
                    # If all lessons are completed, mark topic as completed
                    if completed_lessons == len(lesson_ids):
                        completed_topics += 1
            
            result.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "image_url": course.image_url,
                "is_locked": course.is_locked,
                "total_topics": total_topics,
                "completed_topics": completed_topics
            })
            
        return result
    
    def get_course_with_topics(self, course_id, user_id=None):
        course = self.db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            return None
            
        # Format response
        topics = []
        for topic in course.topics:
            # Count total lessons
            total_lessons = len(topic.lessons)
            
            # Count completed lessons
            completed_lessons = 0
            if user_id:
                lesson_ids = [lesson.id for lesson in topic.lessons]
                if lesson_ids:
                    completed_lessons = self.db.query(UserProgress).filter(
                        UserProgress.user_id == user_id,
                        UserProgress.lesson_id.in_(lesson_ids),
                        UserProgress.is_completed == True
                    ).count()
            
            topics.append({
                "id": topic.id,
                "title": topic.title,
                "description": topic.description,
                "is_locked": topic.is_locked,
                "lessons_count": total_lessons,
                "completed_lessons": completed_lessons
            })
            
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "image_url": course.image_url,
            "is_locked": course.is_locked,
            "topics": topics
        }