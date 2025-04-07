# app/models/challenge.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class CodingChallenge(Base):
    __tablename__ = "coding_challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    starter_code = Column(Text, nullable=False)
    solution_code = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    hints = Column(Text, nullable=True)  # Store as JSON string
    points = Column(Integer, default=10)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

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