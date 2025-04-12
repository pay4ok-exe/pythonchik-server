# app/schemas/game.py
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

class GameBase(BaseModel):
    title: str
    slug: str
    description: str
    short_description: Optional[str] = None
    image_url: Optional[str] = None
    difficulty: str
    category: str
    xp_reward: int
    estimated_time: Optional[str] = None

class GameCreate(GameBase):
    pass

class GameResponse(GameBase):
    id: int
    unlocked: bool = False
    is_started: Optional[bool] = False
    is_completed: Optional[bool] = False
    current_level: Optional[int] = 0
    score: Optional[int] = 0
    last_played_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    class Config:
        orm_mode = True

class GameDetailResponse(GameResponse):
    saved_data: Optional[Dict[str, Any]] = {}
    
    class Config:
        orm_mode = True

class GameProgressUpdate(BaseModel):
    is_started: Optional[bool] = None
    is_completed: Optional[bool] = None
    current_level: Optional[int] = None
    score: Optional[int] = None
    data: Optional[Dict[str, Any]] = None

class GameProgressResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    is_started: bool
    is_completed: bool
    current_level: int
    score: int
    last_played_at: Optional[str] = None
    completed_at: Optional[str] = None
    data: Optional[Dict[str, Any]] = {}
    
    class Config:
        orm_mode = True