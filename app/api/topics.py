from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.topic import TopicDetailResponse
from app.services.topic import TopicService
from app.utils.database import get_db

router = APIRouter(prefix="/topics", tags=["topics"])

@router.get("/{topic_id}", response_model=TopicDetailResponse)
async def get_topic(
    topic_id: int,
    user_id: int = None,  # Optional, for getting user progress
    db: Session = Depends(get_db)
):
    topic_service = TopicService(db)
    topic = topic_service.get_topic_with_lessons(topic_id, user_id)
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
        
    return topic