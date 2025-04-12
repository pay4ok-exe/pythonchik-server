# app/api/game.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.services.game import GameService
from app.utils.database import get_db
from app.schemas.game import GameResponse, GameDetailResponse, GameProgressUpdate, GameProgressResponse

router = APIRouter(prefix="/game", tags=["game"])

@router.get("", response_model=List[GameResponse])
async def get_games(
    user_id: Optional[int] = Query(None),
    difficulty: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all games with optional filters
    """
    game_service = GameService(db)
    games = game_service.get_all_games(user_id)
    
    # Apply filters if provided
    if difficulty:
        games = [g for g in games if g["difficulty"].lower() == difficulty.lower()]
    
    if category:
        games = [g for g in games if g["category"].lower() == category.lower()]
    
    return games

@router.get("/{slug}", response_model=GameDetailResponse)
async def get_game(
    slug: str,
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get a specific game by slug
    """
    game_service = GameService(db)
    game = game_service.get_game_by_slug(slug, user_id)
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return game

@router.post("/{game_id}/progress", response_model=GameProgressResponse)
async def update_game_progress(
    game_id: int,
    progress: GameProgressUpdate,
    current_user = Depends(AuthService().get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a user's progress for a specific game
    """
    game_service = GameService(db)
    
    # Check if game exists
    game = game_service.game_repo.get_game_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Update progress
    result = game_service.update_game_progress(
        user_id=current_user.id,
        game_id=game_id,
        progress_data=progress.dict()
    )
    
    return result   