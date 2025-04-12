# app/models/game.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    difficulty = Column(String(20), nullable=False)  # 'beginner', 'intermediate', 'advanced'
    category = Column(String(50), nullable=False)  # 'adventure', 'puzzle', 'quest', etc.
    xp_reward = Column(Integer, default=100)
    estimated_time = Column(String(50), nullable=True)  # '30 minutes', '1 hour', etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user_progress = relationship("UserGameProgress", back_populates="game")

class UserGameProgress(Base):
    __tablename__ = "user_game_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    is_started = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    current_level = Column(Integer, default=0)
    score = Column(Integer, default=0)
    data = Column(Text, nullable=True)  # JSON data with game-specific progress
    last_played_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="game_progress")
    game = relationship("Game", back_populates="user_progress")

    # Add unique constraint for user_id and game_id
    __table_args__ = (
        UniqueConstraint('user_id', 'game_id', name='uq_user_game'),
    )