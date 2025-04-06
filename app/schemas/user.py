from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str

class UserResponse(UserBase):
    id: int
    level: int
    experience: int
    coins: int
    streak: int
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None