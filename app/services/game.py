# app/services/game.py - Update the existing service
from typing import Dict, List, Any, Optional
import json
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.challenge import ChallengeRepository
from app.repositories.user import UserRepository

class GameService:
    def __init__(self, db: Session):
        self.db = db
        self.challenge_repo = ChallengeRepository(db)
        self.user_repo = UserRepository(db)
    
    def get_game_challenges(self, difficulty: str = "beginner") -> List[Dict[str, Any]]:
        """
        Get a list of coding challenges based on difficulty level.
        
        Args:
            difficulty: Difficulty level (beginner, intermediate, advanced)
            
        Returns:
            List of challenge dictionaries
        """
        challenges = self.challenge_repo.get_all_challenges(difficulty)
        
        # Convert to dictionary format and parse hints
        result = []
        for challenge in challenges:
            challenge_dict = {
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "starter_code": challenge.starter_code,
                "expected_output": challenge.expected_output,
                "hints": json.loads(challenge.hints) if challenge.hints else [],
                "points": challenge.points
            }
            result.append(challenge_dict)
            
        return result
    
    def evaluate_challenge(self, user_id: int, challenge_id: int, code: str, output: str) -> Dict[str, Any]:
        """
        Evaluate a user's solution to a challenge.
        
        Args:
            user_id: ID of the user
            challenge_id: ID of the challenge
            code: User's code
            output: Output produced by the code
            
        Returns:
            Evaluation result
        """
        # Get the user
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}
        
        # Get the challenge
        challenge = self.challenge_repo.get_challenge_by_id(challenge_id)
        if not challenge:
            return {"success": False, "error": "Challenge not found"}
        
        # Check if the output matches the expected output
        correct = output.strip() == challenge.expected_output.strip()
        
        # Record the challenge attempt
        self.challenge_repo.record_challenge_attempt(
            user_id=user_id,
            challenge_id=challenge_id,
            code_submitted=code,
            completed=correct
        )
        
        # If correct, award points
        if correct and user:
            user.experience += challenge.points
            user.coins += challenge.points // 2
            self.db.commit()
        
        return {
            "success": True,
            "correct": correct,
            "points_earned": challenge.points if correct else 0,
            "coins_earned": challenge.points // 2 if correct else 0,
            "expected_output": challenge.expected_output
        }