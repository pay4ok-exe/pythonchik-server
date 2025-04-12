# scripts/seed_courses.py
import sys
import os
import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Add parent directory to path to import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.course import Course
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.quiz import QuizQuestion, QuizOption
from app.utils.database import SessionLocal

def seed_courses():
    db = SessionLocal()
    
    try:
        # Read mock data
        mock_file_path = os.path.join(os.path.dirname(__file__), '..', 'mock.json')
        
        with open(mock_file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
        
        # Process courses
        for course_data in data["courses"]:
            # Check if course already exists
            existing_course = db.query(Course).filter(Course.id == course_data["id"]).first()
            
            if existing_course:
                print(f"Course '{course_data['title']}' already exists. Skipping.")
                continue
            
            # Create new course
            course = Course(
                id=course_data["id"],
                title=course_data["title"],
                description=course_data["description"],
                image_url=course_data.get("image", ""),
                order_index=course_data["id"],
                is_locked=course_data["id"] != 1  # First course is unlocked
            )
            db.add(course)
            db.flush()
            
            print(f"Added course: {course.title}")
            
            # Process topics
            for topic_index, topic_data in enumerate(course_data["topics"]):
                topic = Topic(
                    id=topic_data["id"],
                    course_id=course.id,
                    title=topic_data["title"],
                    description=topic_data["description"],
                    order_index=topic_index,
                    is_locked=topic_index > 0  # First topic is unlocked
                )
                db.add(topic)
                db.flush()
                
                print(f"  Added topic: {topic.title}")
                
                # Process lessons
                for lesson_index, lesson_data in enumerate(topic_data["lessons"]):
                    lesson = Lesson(
                        id=lesson_data["id"],
                        topic_id=topic.id,
                        title=lesson_data["title"],
                        type=lesson_data["type"],
                        content=json.dumps(lesson_data.get("content", [])) if lesson_data.get("content") else None,
                        task=lesson_data.get("task"),
                        expected_output=lesson_data.get("expectedOutput"),
                        order_index=lesson_index
                    )
                    db.add(lesson)
                    db.flush()
                    
                    print(f"    Added lesson: {lesson.title}")
                    
                    # Add quiz questions if it's a quiz lesson
                    if lesson_data["type"] == "quiz" and "questions" in lesson_data:
                        for q_index, question_text in enumerate(lesson_data["questions"]):
                            quiz_question = QuizQuestion(
                                lesson_id=lesson.id,
                                question=question_text,
                                order_index=q_index
                            )
                            db.add(quiz_question)
                            db.flush()
                            
                            # Add some dummy options
                            options = [
                                {"text": f"Option 1 for {question_text}", "is_correct": True},
                                {"text": f"Option 2 for {question_text}", "is_correct": False},
                                {"text": f"Option 3 for {question_text}", "is_correct": False},
                                {"text": f"Option 4 for {question_text}", "is_correct": False}
                            ]
                            
                            for opt_index, opt_data in enumerate(options):
                                quiz_option = QuizOption(
                                    question_id=quiz_question.id,
                                    option_text=opt_data["text"],
                                    is_correct=opt_data["is_correct"],
                                    order_index=opt_index
                                )
                                db.add(quiz_option)
        
        # Commit all changes
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()