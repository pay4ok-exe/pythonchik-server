from typing import List, Optional, Any
from pydantic import BaseModel

class ContentItem(BaseModel):
    title: str
    description: str
    image: Optional[str] = None

class LessonBase(BaseModel):
    title: str
    type: str

class LessonResponse(LessonBase):
    id: int
    is_completed: Optional[bool] = False
    
    class Config:
        orm_mode = True

class LessonDetailResponse(LessonBase):
    id: int
    topic_id: int
    content: Optional[List[ContentItem]] = None
    task: Optional[str] = None
    expected_output: Optional[str] = None
    quiz_questions: Optional[List[Any]] = None
    is_completed: Optional[bool] = False
    
    class Config:
        orm_mode = True

class CompleteLessonRequest(BaseModel):
    user_id: int
    score: Optional[int] = None