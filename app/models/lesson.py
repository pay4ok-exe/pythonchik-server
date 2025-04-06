from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.utils.database import Base
import json

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # 'lesson', 'quiz', 'coding'
    content_json = Column(Text)  # Store content as JSON string
    task = Column(Text)  # For coding lessons
    expected_output = Column(Text)  # For coding lessons
    order_index = Column(Integer, nullable=False)
    xp_reward = Column(Integer, default=10)
    coins_reward = Column(Integer, default=5)
    estimated_time_minutes = Column(Integer, default=10)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    topic = relationship("Topic", back_populates="lessons")
    quiz_questions = relationship("QuizQuestion", back_populates="lesson", cascade="all, delete-orphan")
    user_progress = relationship("UserProgress", back_populates="lesson")

    @property
    def content(self):
        """Deserialize JSON content"""
        if self.content_json:
            return json.loads(self.content_json)
        return []

    @content.setter
    def content(self, content_list):
        """Serialize content to JSON"""
        self.content_json = json.dumps(content_list)