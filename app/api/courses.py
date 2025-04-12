# app/api/courses.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.models.course import Course
from app.models.topic import Topic
from app.schemas.course import CourseResponse, CourseListResponse
from app.services.course import CourseService
from app.utils.database import get_db

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("", response_model=List[CourseListResponse])
async def get_courses(
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        course_service = CourseService(db)
        courses = course_service.get_all_courses(user_id)
        return courses
    except Exception as e:
        # Log the error
        print(f"Error in get_courses endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving courses: {str(e)}"
        )

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        course_service = CourseService(db)
        course = course_service.get_course_with_topics(course_id, user_id)
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
            
        return course
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error
        print(f"Error in get_course endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving course: {str(e)}"
        )