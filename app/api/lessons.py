from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.lesson import LessonDetailResponse, CompleteLessonRequest
from app.services.lesson import LessonService
from app.utils.database import get_db

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/{lesson_id}", response_model=LessonDetailResponse)
async def get_lesson(
    lesson_id: int,
    user_id: int = None,  # Optional, for getting user progress
    db: Session = Depends(get_db)
):
    lesson_service = LessonService(db)
    lesson = lesson_service.get_lesson_detail(lesson_id, user_id)
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
        
    return lesson

@router.post("/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    request: CompleteLessonRequest,
    db: Session = Depends(get_db)
):
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