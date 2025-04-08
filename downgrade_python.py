# downgrade_python.py
import subprocess
import sys
import os

def main():
    print("🛠️ Pythonchick Backend Python Downgrade Utility 🛠️")
    print("===================================================")
    
    # Check current Python version
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"Current Python version: {current_version}")
    
    if sys.version_info.major == 3 and sys.version_info.minor >= 12:
        print("\n⚠️ Python 3.12+ detected. Some packages may not be compatible.")
        print("This utility will set up a Python 3.10 virtual environment.\n")
        
        # Check if Python 3.10 is installed
        try:
            # Try to run python 3.10
            result = subprocess.run(["py", "-3.10", "--version"], 
                                   capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                print("✅ Python 3.10 is installed.")
                python_cmd = "py -3.10"
            else:
                print("❌ Python 3.10 is not installed.")
                print("\nPlease install Python 3.10 from https://www.python.org/downloads/release/python-31011/")
                print("After installation, run this script again.")
                return
        except Exception:
            print("❌ Unable to detect Python 3.10.")
            print("\nPlease install Python 3.10 from https://www.python.org/downloads/release/python-31011/")
            print("After installation, run this script again.")
            return
        
        # Create venv with Python 3.10
        print("\nCreating Python 3.10 virtual environment...")
        venv_cmd = f"{python_cmd} -m venv venv-3.10"
        subprocess.run(venv_cmd, shell=True)
        
        # Install dependencies
        print("\nInstalling compatible dependencies...")
        
        # Create compatible requirements file
        with open("requirements-3.10.txt", "w") as f:
            f.write("""fastapi==0.95.2
uvicorn==0.22.0
sqlalchemy==1.4.46
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
python-multipart==0.0.6
email-validator==2.0.0
python-dotenv==1.0.0
pydantic==1.10.8
""")
        
        if os.name == 'nt':  # Windows
            pip_cmd = "venv-3.10\\Scripts\\pip install -r requirements-3.10.txt"
        else:  # Unix/Mac
            pip_cmd = "venv-3.10/bin/pip install -r requirements-3.10.txt"
            
        subprocess.run(pip_cmd, shell=True)
        
        # Create a launcher script
        if os.name == 'nt':  # Windows
            with open("run-app.bat", "w") as f:
                f.write("@echo off\n")
                f.write("echo Starting Pythonchick API using Python 3.10...\n")
                f.write("venv-3.10\\Scripts\\python run.py --reload\n")
                f.write("pause\n")
        else:  # Unix/Mac
            with open("run-app.sh", "w") as f:
                f.write("#!/bin/bash\n")
                f.write("echo Starting Pythonchick API using Python 3.10...\n")
                f.write("./venv-3.10/bin/python run.py --reload\n")
            os.chmod("run-app.sh", 0o755)
        
        # Fix database config
        print("\nUpdating database configuration to use SQLite...")
        os.makedirs("app/utils", exist_ok=True)
        
        with open("app/utils/database.py", "w") as f:
            f.write("""# app/utils/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy engine with SQLite for simplicity
engine = create_engine(
    "sqlite:///./pythonchick.db", 
    connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")
        
        with open("app/config.py", "w") as f:
            f.write("""# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pythonchick API"
    
    # Security
    SECRET_KEY: str = "u-know-who-am-i"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Database - Using SQLite for simplicity
    DATABASE_URL: str = "sqlite:///./pythonchick.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
""")
        
        print("\n✅ Setup completed!")
        print("\nTo start the API server, run:")
        if os.name == 'nt':  # Windows
            print("  run-app.bat")
        else:  # Unix/Mac
            print("  ./run-app.sh")
        
    else:
        print(f"\nYour Python version ({current_version}) should be compatible with the requirements.")
        print("Please make sure you have properly installed the dependencies:")
        print("  1. Create a virtual environment: python -m venv venv")
        print("  2. Activate it and install: pip install -r requirements.txt")
        print("  3. Run the app: python run.py")

if __name__ == "__main__":
    main()