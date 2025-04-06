from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.services.lesson import LessonService
from app.utils.database import get_db

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    score: int = None,
    current_user = Depends(AuthService().get_current_user),
    db: Session = Depends(get_db)
):
    lesson_service = LessonService(db)
    result = lesson_service.complete_lesson(
        lesson_id=lesson_id,
        user_id=current_user.id,
        score=score
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
        
    return result