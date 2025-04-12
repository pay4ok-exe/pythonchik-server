# app/api/lessons.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.lesson import LessonDetailResponse, CompleteLessonRequest
from app.services.lesson import LessonService
from app.utils.database import get_db

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/{lesson_id}", response_model=LessonDetailResponse)
async def get_lesson(
    lesson_id: int,
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        lesson_service = LessonService(db)
        lesson = lesson_service.get_lesson_detail(lesson_id, user_id)
        
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
            
        return lesson
    except Exception as e:
        # Log the error
        print(f"Error in get_lesson endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving lesson: {str(e)}"
        )

@router.post("/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    request: CompleteLessonRequest,
    db: Session = Depends(get_db)
):
    try:
        lesson_service = LessonService(db)
        result = lesson_service.complete_lesson(
            lesson_id=lesson_id,
            user_id=request.user_id,
            score=request.score
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
            
        return {"message": "Lesson completed successfully", "xp_earned": result.get("xp_earned")}
    except Exception as e:
        # Log the error
        print(f"Error in complete_lesson endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error completing lesson: {str(e)}"
        )