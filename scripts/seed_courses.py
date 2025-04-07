# scripts/seed_courses.py
import sys
import os
import json
from sqlalchemy.orm import Session
import os.path

# Add parent directory to path to import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.course import Course
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.coding_challenge import CodingChallenge
from app.models.quiz import QuizQuestion, QuizOption
from app.utils.database import SessionLocal

def seed_courses():
    db = SessionLocal()
    
    try:
        # Check if mock.json exists
        mock_file_path = "mock.json"
        if not os.path.isfile(mock_file_path):
            print(f"Error: File '{mock_file_path}' not found.")
            return
            
        # Read mock data
        with open(mock_file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
        
        # Process courses
        for course_data in data["courses"]:
            # Check if course already exists (based on ID)
            existing_course = db.query(Course).filter(Course.id == course_data["id"]).first()
            
            if existing_course:
                print(f"Course '{course_data['title']}' already exists. Skipping.")
                continue
            
            # Create new course
            course = Course(
                id=course_data["id"],
                title=course_data["title"],
                description=course_data["description"],
                image_url=course_data["image"],
                order_index=course_data["id"],  # Using ID as order index for simplicity
                is_locked=course_data["id"] != 1  # First course is unlocked by default
            )
            db.add(course)
            db.flush()  # Flush to get the ID
            
            print(f"Added course: {course.title}")
            
            # Process topics
            for i, topic_data in enumerate(course_data["topics"]):
                topic = Topic(
                    id=topic_data["id"],
                    course_id=course.id,
                    title=topic_data["title"],
                    description=topic_data["description"],
                    order_index=i,
                    is_locked=i > 0  # First topic is unlocked by default
                )
                db.add(topic)
                db.flush()
                
                print(f"  Added topic: {topic.title}")
                
                # Process lessons
                for j, lesson_data in enumerate(topic_data["lessons"]):
                    lesson_type = lesson_data["type"]
                    
                    # Create lesson
                    lesson = Lesson(
                        id=lesson_data["id"],
                        topic_id=topic.id,
                        title=lesson_data["title"],
                        type=lesson_type,
                        order_index=j,
                        xp_reward=10,  # Default values
                        coins_reward=5
                    )
                    
                    # Add type-specific data
                    if lesson_type == "lesson":
                        lesson.parsed_content = lesson_data.get("content", [])

                    db.add(lesson)
                    db.flush()
                    
                    print(f"    Added lesson: {lesson.title}")

                    if lesson_type == "coding":
                        coding_challenge = CodingChallenge(
                            lesson_id=lesson.id,
                            instructions=lesson_data.get("task", ""),
                            expected_output=lesson_data.get("expectedOutput", ""),
                            solution_code="",
                            initial_code=""
                        )
                        db.add(coding_challenge)
                        db.flush()
                    
                    # Add quiz questions if this is a quiz lesson
                    if lesson_type == "quiz" and "questions" in lesson_data:
                        for k, question_text in enumerate(lesson_data["questions"]):
                            question = QuizQuestion(
                                lesson_id=lesson.id,
                                question=question_text,
                                order_index=k
                            )
                            db.add(question)
                            db.flush()
                            
                            # Add dummy options for now (in a real app, you'd have actual options)
                            for m in range(4):
                                option = QuizOption(
                                    question_id=question.id,
                                    option_text=f"Option {m+1} for {question_text}",
                                    is_correct=m == 0,  # First option is correct by default
                                    order_index=m
                                )
                                db.add(option)
            
            # Commit after each course
            db.commit()
            print(f"Committed data for course: {course.title}")
        
        print("Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()