from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.topic import TopicResponse

class CourseBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    
class CourseListResponse(CourseBase):
    id: int
    is_locked: bool
    total_topics: int
    completed_topics: Optional[int] = 0

    class Config:
        orm_mode = True

class CourseResponse(CourseBase):
    id: int
    is_locked: bool
    topics: List[TopicResponse] = []
    
    class Config:
        orm_mode = True