# scripts/seed_games.py
import sys
import os
from pathlib import Path

# Add parent directory to path to import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.repositories.game import GameRepository
from app.utils.database import SessionLocal

def seed_games():
    db = SessionLocal()
    
    try:
        game_repo = GameRepository(db)
        
        # Define initial games
        games = [
            {
                "title": "Python Adventure",
                "slug": "python-adventure",
                "description": "Embark on a journey through a magical world where you solve Python puzzles to proceed to the next level.",
                "short_description": "Solve Python puzzles in a magical world",
                "image_url": "/games/python-adventure.png",
                "difficulty": "Beginner",
                "category": "adventure",
                "xp_reward": 150,
                "estimated_time": "30 minutes"
            },
            {
                "title": "Code Quest",
                "slug": "code-quest",
                "description": "Choose your character and embark on a quest to collect coding gems by solving Python challenges.",
                "short_description": "Collect gems by solving Python challenges",
                "image_url": "/games/code-quest.png",
                "difficulty": "Beginner",
                "category": "quest",
                "xp_reward": 200,
                "estimated_time": "45 minutes"
            },
            {
                "title": "Function Factory",
                "slug": "function-factory",
                "description": "Build and operate a function factory! Define Python functions to automate various processes in your growing factory.",
                "short_description": "Build a factory using Python functions",
                "image_url": "/games/function-factory.png",
                "difficulty": "Intermediate",
                "category": "simulation",
                "xp_reward": 250,
                "estimated_time": "1 hour"
            },
            {
                "title": "Bug Hunter",
                "slug": "bug-hunter",
                "description": "Track down and eliminate bugs in Python code! Use your debugging skills to fix broken code.",
                "short_description": "Fix bugs in Python code",
                "image_url": "/games/bug-hunter.png",
                "difficulty": "Intermediate",
                "category": "puzzle",
                "xp_reward": 300,
                "estimated_time": "45 minutes"
            },
            {
                "title": "Data Explorer",
                "slug": "data-explorer",
                "description": "Embark on a data science adventure where you analyze data to discover hidden treasures.",
                "short_description": "Analyze data to find treasures",
                "image_url": "/games/data-explorer.png",
                "difficulty": "Advanced",
                "category": "data-science",
                "xp_reward": 350,
                "estimated_time": "1.5 hours"
            }
        ]
        
        # Create each game
        for game_data in games:
            # Check if game already exists (based on slug)
            existing_game = game_repo.get_game_by_slug(game_data["slug"])
            
            if existing_game:
                print(f"Game '{game_data['title']}' already exists. Skipping.")
                continue
            
            # Create new game
            game = game_repo.create_game(
                title=game_data["title"],
                slug=game_data["slug"],
                description=game_data["description"],
                short_description=game_data["short_description"],
                image_url=game_data["image_url"],
                difficulty=game_data["difficulty"],
                category=game_data["category"],
                xp_reward=game_data["xp_reward"],
                estimated_time=game_data["estimated_time"]
            )
            
            print(f"Added game: {game.title}")
        
        print("Database seeded with games successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_games()