# app/repositories/game.py
from sqlalchemy.orm import Session
from app.models.game import Game, UserGameProgress
from typing import List, Optional
import json
from datetime import datetime

class GameRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_games(self) -> List[Game]:
        """Get all active games"""
        return self.db.query(Game).filter(Game.is_active == True).all()
    
    def get_game_by_id(self, game_id: int) -> Optional[Game]:
        """Get a specific game by ID"""
        return self.db.query(Game).filter(Game.id == game_id).first()
    
    def get_game_by_slug(self, slug: str) -> Optional[Game]:
        """Get a specific game by slug"""
        return self.db.query(Game).filter(Game.slug == slug).first()
    
    def create_game(self, 
                    title: str, 
                    slug: str,
                    description: str,
                    short_description: str,
                    image_url: str,
                    difficulty: str,
                    category: str,
                    xp_reward: int,
                    estimated_time: str) -> Game:
        """Create a new game"""
        game = Game(
            title=title,
            slug=slug,
            description=description,
            short_description=short_description,
            image_url=image_url,
            difficulty=difficulty,
            category=category,
            xp_reward=xp_reward,
            estimated_time=estimated_time
        )
        
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        
        return game
    
    def get_user_game_progress(self, user_id: int, game_id: int) -> Optional[UserGameProgress]:
        """Get a user's progress for a specific game"""
        return self.db.query(UserGameProgress).filter(
            UserGameProgress.user_id == user_id,
            UserGameProgress.game_id == game_id
        ).first()
    
    def get_user_games_progress(self, user_id: int) -> List[UserGameProgress]:
        """Get all games progress for a user"""
        return self.db.query(UserGameProgress).filter(
            UserGameProgress.user_id == user_id
        ).all()
    
    def update_game_progress(self, 
                           user_id: int, 
                           game_id: int, 
                           is_started: bool = None,
                           is_completed: bool = None,
                           current_level: int = None,
                           score: int = None,
                           data: dict = None) -> UserGameProgress:
        """Update a user's game progress"""
        progress = self.get_user_game_progress(user_id, game_id)
        
        if not progress:
            # Create new progress record
            progress = UserGameProgress(
                user_id=user_id,
                game_id=game_id,
                is_started=is_started if is_started is not None else True,
                is_completed=is_completed if is_completed is not None else False,
                current_level=current_level if current_level is not None else 0,
                score=score if score is not None else 0,
                data=json.dumps(data) if data else None,
                last_played_at=datetime.utcnow()
            )
            self.db.add(progress)
        else:
            # Update existing progress
            if is_started is not None:
                progress.is_started = is_started
            
            if is_completed is not None:
                progress.is_completed = is_completed
                if is_completed:
                    progress.completed_at = datetime.utcnow()
            
            if current_level is not None:
                progress.current_level = current_level
            
            if score is not None:
                progress.score = score
            
            if data is not None:
                # Merge with existing data if any
                existing_data = {}
                if progress.data:
                    try:
                        existing_data = json.loads(progress.data)
                    except:
                        existing_data = {}
                
                merged_data = {**existing_data, **data}
                progress.data = json.dumps(merged_data)
            
            progress.last_played_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(progress)
        
        return progress