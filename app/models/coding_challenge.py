from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from app.utils.database import Base

class CodingChallenge(Base):
    __tablename__ = "coding_challenges"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    instructions = Column(Text, nullable=False)
    initial_code = Column(Text)
    solution_code = Column(Text, default="")
    expected_output = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
