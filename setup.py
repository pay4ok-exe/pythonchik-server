import sys
import traceback

def debug_imports():
    try:
        # Import core libraries
        import fastapi
        import pydantic
        import sqlalchemy
        
        # Print versions
        print("FastAPI version:", fastapi.__version__)
        print("Pydantic version:", pydantic.__version__)
        print("SQLAlchemy version:", sqlalchemy.__version__)
        
        # Try importing your project modules
        from app import main
        from app import config
        from app.models import user, course, topic, lesson
        
        print("All imports successful!")
    
    except Exception as e:
        print(f"Import error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_imports()