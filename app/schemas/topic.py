from typing import List, Optional
from pydantic import BaseModel
from app.schemas.lesson import LessonResponse

class TopicBase(BaseModel):
    title: str
    description: str

class TopicResponse(TopicBase):
    id: int
    is_locked: bool
    lessons_count: int
    completed_lessons: Optional[int] = 0
    
    class Config:
        orm_mode = True

class TopicDetailResponse(TopicBase):
    id: int
    is_locked: bool
    course_id: int
    lessons: List[LessonResponse] = []
    
    class Config:
        orm_mode = True