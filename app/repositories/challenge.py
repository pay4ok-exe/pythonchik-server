# app/repositories/challenge.py
from sqlalchemy.orm import Session
from app.models.challenge import CodingChallenge, UserChallenge
from typing import List, Optional
import json
import datetime

class ChallengeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_challenges(self, difficulty: str = None) -> List[CodingChallenge]:
        """Get all coding challenges, optionally filtered by difficulty"""
        query = self.db.query(CodingChallenge)
        
        if difficulty:
            query = query.filter(CodingChallenge.difficulty == difficulty)
            
        return query.all()
    
    def get_challenge_by_id(self, challenge_id: int) -> Optional[CodingChallenge]:
        """Get a specific challenge by ID"""
        return self.db.query(CodingChallenge).filter(CodingChallenge.id == challenge_id).first()
    
    def create_challenge(self, 
                         title: str, 
                         description: str, 
                         difficulty: str,
                         starter_code: str,
                         solution_code: str,
                         expected_output: str,
                         hints: List[str] = None,
                         points: int = 10) -> CodingChallenge:
        """Create a new coding challenge"""
        hints_json = json.dumps(hints) if hints else json.dumps([])
        
        challenge = CodingChallenge(
            title=title,
            description=description,
            difficulty=difficulty,
            starter_code=starter_code,
            solution_code=solution_code,
            expected_output=expected_output,
            hints=hints_json,
            points=points
        )
        
        self.db.add(challenge)
        self.db.commit()
        self.db.refresh(challenge)
        
        return challenge
    
    def get_user_challenge(self, user_id: int, challenge_id: int) -> Optional[UserChallenge]:
        """Get a user's attempt at a specific challenge"""
        return self.db.query(UserChallenge).filter(
            UserChallenge.user_id == user_id,
            UserChallenge.challenge_id == challenge_id
        ).first()
    
    def record_challenge_attempt(self, 
                                user_id: int, 
                                challenge_id: int, 
                                code_submitted: str,
                                completed: bool = False) -> UserChallenge:
        """Record a user's attempt at a challenge"""
        user_challenge = self.get_user_challenge(user_id, challenge_id)
        
        if user_challenge:
            user_challenge.attempts += 1
            user_challenge.code_submitted = code_submitted
            
            if completed and not user_challenge.completed:
                user_challenge.completed = True
                user_challenge.completed_at = datetime.datetime.utcnow()
        else:
            user_challenge = UserChallenge(
                user_id=user_id,
                challenge_id=challenge_id,
                code_submitted=code_submitted,
                attempts=1,
                completed=completed,
                completed_at=datetime.datetime.utcnow() if completed else None
            )
            self.db.add(user_challenge)
            
        self.db.commit()
        self.db.refresh(user_challenge)
        
        return user_challenge