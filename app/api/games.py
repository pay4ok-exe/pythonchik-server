# app/api/games.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.services.game import GameService
from app.services.code_execution import CodeExecutionService
from app.utils.database import get_db

router = APIRouter(prefix="/games", tags=["games"])

class ChallengeResponse(BaseModel):
    id: str
    title: str
    description: str
    starter_code: str
    hints: List[str]
    points: int

class ChallengeSubmission(BaseModel):
    challenge_id: str
    code: str

class ChallengeEvaluationResponse(BaseModel):
    success: bool
    correct: bool
    points_earned: int
    coins_earned: int
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

@router.get("/challenges", response_model=List[ChallengeResponse])
async def get_challenges(
    difficulty: Optional[str] = "beginner",
    current_user = Depends(AuthService().get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a list of coding challenges based on difficulty.
    """
    game_service = GameService(db)
    challenges = game_service.get_game_challenges(difficulty)
    
    # Remove expected_output from response to avoid giving away the answer
    for challenge in challenges:
        challenge.pop("expected_output", None)
    
    return challenges

@router.post("/challenges/submit", response_model=ChallengeEvaluationResponse)
async def submit_challenge(
    submission: ChallengeSubmission,
    current_user = Depends(AuthService().get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a solution to a coding challenge.
    """
    # Execute the code
    execution_service = CodeExecutionService()
    execution_result = execution_service.execute_code(submission.code)
    
    if not execution_result["success"]:
        return {
            "success": False,
            "correct": False,
            "points_earned": 0,
            "coins_earned": 0,
            "output": execution_result.get("output", ""),
            "error": execution_result.get("error", ""),
            "execution_time": execution_result.get("execution_time", 0)
        }
    
    # Evaluate the challenge
    game_service = GameService(db)
    evaluation = game_service.evaluate_challenge(
        user_id=current_user.id,
        challenge_id=submission.challenge_id,
        code=submission.code,
        output=execution_result["output"]
    )
    
    return {
        "success": True,
        "correct": evaluation.get("correct", False),
        "points_earned": evaluation.get("points_earned", 0),
        "coins_earned": evaluation.get("coins_earned", 0),
        "output": execution_result.get("output", ""),
        "error": execution_result.get("error", ""),
        "execution_time": execution_result.get("execution_time", 0)
    }