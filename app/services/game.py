# app/services/game.py
from sqlalchemy.orm import Session
import json
from typing import List, Dict, Any, Optional
from app.repositories.game import GameRepository
from app.repositories.user import UserRepository
from app.models.user import User

class GameService:
    def __init__(self, db: Session):
        self.db = db
        self.game_repo = GameRepository(db)
        self.user_repo = UserRepository(db)
    
    def get_all_games(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all games with optional user progress
        
        Args:
            user_id: Optional user ID to include progress info
            
        Returns:
            List of game dictionaries with progress info if user_id provided
        """
        games = self.game_repo.get_all_games()
        result = []
        
        # If user_id is provided, fetch progress for each game
        user_progress = {}
        if user_id:
            progress_list = self.game_repo.get_user_games_progress(user_id)
            user_progress = {p.game_id: p for p in progress_list}
        
        for game in games:
            game_dict = {
                "id": game.id,
                "title": game.title,
                "slug": game.slug,
                "description": game.description,
                "short_description": game.short_description,
                "image_url": game.image_url,
                "difficulty": game.difficulty,
                "category": game.category,
                "xp_reward": game.xp_reward,
                "estimated_time": game.estimated_time
            }
            
            # Add progress info if user_id was provided
            if user_id:
                progress = user_progress.get(game.id)
                if progress:
                    game_dict["is_started"] = progress.is_started
                    game_dict["is_completed"] = progress.is_completed
                    game_dict["current_level"] = progress.current_level
                    game_dict["score"] = progress.score
                    game_dict["last_played_at"] = progress.last_played_at.isoformat() if progress.last_played_at else None
                    game_dict["completed_at"] = progress.completed_at.isoformat() if progress.completed_at else None
                else:
                    game_dict["is_started"] = False
                    game_dict["is_completed"] = False
                    game_dict["current_level"] = 0
                    game_dict["score"] = 0
                    game_dict["last_played_at"] = None
                    game_dict["completed_at"] = None
            
            # Determine if game is unlocked (first game or previous games completed)
            game_dict["unlocked"] = True if game.id == 1 else False
            
            result.append(game_dict)
        
        # Mark games as unlocked based on previous game completion
        for i in range(1, len(result)):
            if user_id and result[i-1].get("is_completed", False):
                result[i]["unlocked"] = True
        
        return result
    
    def get_game_by_slug(self, slug: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get game details by slug with optional user progress
        
        Args:
            slug: Game slug
            user_id: Optional user ID to include progress info
            
        Returns:
            Game dictionary with progress info if user_id provided
        """
        game = self.game_repo.get_game_by_slug(slug)
        
        if not game:
            return None
        
        result = {
            "id": game.id,
            "title": game.title,
            "slug": game.slug,
            "description": game.description,
            "short_description": game.short_description,
            "image_url": game.image_url,
            "difficulty": game.difficulty,
            "category": game.category,
            "xp_reward": game.xp_reward,
            "estimated_time": game.estimated_time
        }
        
        # Add progress info if user_id was provided
        if user_id:
            progress = self.game_repo.get_user_game_progress(user_id, game.id)
            if progress:
                result["is_started"] = progress.is_started
                result["is_completed"] = progress.is_completed
                result["current_level"] = progress.current_level
                result["score"] = progress.score
                result["last_played_at"] = progress.last_played_at.isoformat() if progress.last_played_at else None
                result["completed_at"] = progress.completed_at.isoformat() if progress.completed_at else None
                
                # Parse saved game data if available
                if progress.data:
                    try:
                        result["saved_data"] = json.loads(progress.data)
                    except:
                        result["saved_data"] = {}
            else:
                result["is_started"] = False
                result["is_completed"] = False
                result["current_level"] = 0
                result["score"] = 0
                result["last_played_at"] = None
                result["completed_at"] = None
                result["saved_data"] = {}
        
        # Determine if game is unlocked
        result["unlocked"] = self._is_game_unlocked(game.id, user_id)
        
        return result
    
    def _is_game_unlocked(self, game_id: int, user_id: Optional[int] = None) -> bool:
        """
        Determine if a game is unlocked for a user
        
        Args:
            game_id: Game ID
            user_id: User ID
            
        Returns:
            Boolean indicating if game is unlocked
        """
        # First game is always unlocked
        if game_id == 1:
            return True
            
        # If no user_id, game is locked (except first game)
        if not user_id:
            return False
        
        # Check if previous game is completed
        prev_game_id = game_id - 1
        progress = self.game_repo.get_user_game_progress(user_id, prev_game_id)
        
        return progress and progress.is_completed
    
    def update_game_progress(self, user_id: int, game_id: int, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a user's game progress
        
        Args:
            user_id: User ID
            game_id: Game ID
            progress_data: Dictionary containing progress data
            
        Returns:
            Updated progress dictionary
        """
        is_started = progress_data.get('is_started')
        is_completed = progress_data.get('is_completed')
        current_level = progress_data.get('current_level')
        score = progress_data.get('score')
        data = progress_data.get('data')
        
        progress = self.game_repo.update_game_progress(
            user_id=user_id,
            game_id=game_id,
            is_started=is_started,
            is_completed=is_completed,
            current_level=current_level,
            score=score,
            data=data
        )
        
        # If game is completed, update user XP
        if is_completed:
            game = self.game_repo.get_game_by_id(game_id)
            if game:
                user = self.user_repo.get_by_id(user_id)
                if user:
                    user.experience += game.xp_reward
                    user.level = (user.experience // 100) + 1
                    self.db.commit()
        
        result = {
            "id": progress.id,
            "user_id": progress.user_id,
            "game_id": progress.game_id,
            "is_started": progress.is_started,
            "is_completed": progress.is_completed,
            "current_level": progress.current_level,
            "score": progress.score,
            "last_played_at": progress.last_played_at.isoformat() if progress.last_played_at else None,
            "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
        }
        
        if progress.data:
            try:
                result["data"] = json.loads(progress.data)
            except:
                result["data"] = {}
        else:
            result["data"] = {}
        
        return result