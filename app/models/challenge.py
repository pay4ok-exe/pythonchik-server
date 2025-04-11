# app/models/challenge.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class CodingChallenge(Base):
    __tablename__ = "coding_challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    difficulty = Column(String(20), nullable=True)  # beginner, intermediate, advanced
    starter_code = Column(Text, nullable=True)
    solution_code = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    hints = Column(Text, nullable=True)  # Store as JSON string
    points = Column(Integer, default=10)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship with lesson (if associated with a specific lesson)
    lesson = relationship("Lesson", back_populates="challenges")

class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("coding_challenges.id"), nullable=False)
    completed = Column(Boolean, default=False)
    code_submitted = Column(Text, nullable=True)
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="challenges")
    challenge = relationship("CodingChallenge")