# app/api/progress.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.services.auth import AuthService, oauth2_scheme
from app.services.lesson import LessonService
from app.utils.database import get_db
from app.models.user import User

router = APIRouter(prefix="/progress", tags=["progress"])

# Create an instance of AuthService for dependency injection
auth_service = AuthService()

@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    score: Optional[int] = Query(None),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    try:
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
    except Exception as e:
        # Log the error
        print(f"Error in progress/complete_lesson endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error completing lesson: {str(e)}"
        )