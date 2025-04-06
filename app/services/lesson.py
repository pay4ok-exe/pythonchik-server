from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.models.user import User
from datetime import datetime

class LessonService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_lesson_detail(self, lesson_id, user_id=None):
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        
        if not lesson:
            return None
            
        # Check if lesson is completed
        is_completed = False
        if user_id:
            progress = self.db.query(UserProgress).filter(
                UserProgress.user_id == user_id,
                UserProgress.lesson_id == lesson.id
            ).first()
            
            if progress and progress.is_completed:
                is_completed = True
                
        # Prepare response based on lesson type
        result = {
            "id": lesson.id,
            "title": lesson.title,
            "type": lesson.type,
            "topic_id": lesson.topic_id,
            "is_completed": is_completed
        }
        
        if lesson.type == "lesson":
            result["content"] = lesson.content
        elif lesson.type == "coding":
            result["task"] = lesson.task
            result["expected_output"] = lesson.expected_output
        elif lesson.type == "quiz":
            # Get quiz questions and options
            result["quiz_questions"] = []
            for question in lesson.quiz_questions:
                options = []
                for option in question.options:
                    options.append({
                        "id": option.id,
                        "text": option.option_text,
                        "is_correct": option.is_correct
                    })
                
                result["quiz_questions"].append({
                    "id": question.id,
                    "question": question.question,
                    "explanation": question.explanation,
                    "options": options
                })
                
        return result
    
    def complete_lesson(self, lesson_id, user_id, score=None):
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        
        if not lesson:
            return None
            
        # Create or update progress record
        progress = self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id == lesson_id
        ).first()
        
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
        xp_earned = lesson.xp_reward
        
        if user:
            user.experience += xp_earned
            user.coins += lesson.coins_reward
            
            # Update level based on experience
            user.level = (user.experience // 100) + 1
            
            # Update streak (simple implementation)
            if not user.last_login_date or (datetime.utcnow().date() - user.last_login_date.date()).days <= 1:
                user.streak += 1
            else:
                user.streak = 1
            
            user.last_login_date = datetime.utcnow()
        
        # Check if all lessons in topic are completed - if so, unlock next topic
        topic = lesson.topic
        all_lesson_ids = [l.id for l in topic.lessons]
        completed_lesson_count = self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id.in_(all_lesson_ids),
            UserProgress.is_completed == True
        ).count()
        
        # If all lessons in topic are completed, unlock next topic
        if completed_lesson_count == len(all_lesson_ids):
            # Get next topic in the same course
            next_topic = self.db.query(Topic).filter(
                Topic.course_id == topic.course_id,
                Topic.order_index == topic.order_index + 1
            ).first()
            
            if next_topic:
                next_topic.is_locked = False
        
        self.db.commit()
        
        return {
            "success": True,
            "xp_earned": xp_earned,
            "coins_earned": lesson.coins_reward,
            "progress": {
                "is_completed": True,
                "score": score,
                "attempts": progress.attempts
            }
        }