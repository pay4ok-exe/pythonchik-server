from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.course import Course
from app.models.topic import Topic
from app.schemas.course import CourseResponse, CourseListResponse
from app.services.course import CourseService
from app.utils.database import get_db

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("", response_model=List[CourseListResponse])
async def get_courses(
    user_id: int = None,  # Optional, for getting user progress
    db: Session = Depends(get_db)
):
    course_service = CourseService(db)
    courses = course_service.get_all_courses(user_id)
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    user_id: int = None,  # Optional, for getting user progress
    db: Session = Depends(get_db)
):
    course_service = CourseService(db)
    course = course_service.get_course_with_topics(course_id, user_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
        
    return course