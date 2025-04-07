# setup.py
import os
import sys
import subprocess

def setup_database():
    """Set up the database tables and seed initial data"""
    print("Setting up database...")
    
    # Initialize database
    subprocess.run([sys.executable, "scripts/init_db.py"])
    
    # Seed courses
    subprocess.run([sys.executable, "scripts/seed_courses.py"])
    
    # Seed challenges
    subprocess.run([sys.executable, "scripts/seed_challenges.py"])
    
    print("Database setup complete!")

def setup_environment():
    """Set up the development environment"""
    print("Setting up environment...")
    
    # Create a .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# Pythonchick Environment Variables\n")
            f.write("API_V1_STR=/api/v1\n")
            f.write("PROJECT_NAME=Pythonchick API\n")
            f.write("SECRET_KEY=your-secret-key-here\n")
            f.write("ALGORITHM=HS256\n")
            f.write("ACCESS_TOKEN_EXPIRE_MINUTES=60\n")
            f.write("DATABASE_URL=mssql+pyodbc://pay4ok\\pay4ok/Pythonchick?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes\n")
        
        print("Created .env file with default settings")
    else:
        print(".env file already exists")
    
    print("Environment setup complete!")

def main():
    """Main setup function"""
    print("Pythonchick Setup")
    print("=================")
    
    setup_environment()
    setup_database()
    
    print("\nSetup completed successfully!")
    print("To start the API server, run: python run.py --reload")
    print("To start the frontend, run: cd frontend && npm start")

if __name__ == "__main__":
    main()