# setup.py
import os
import sys
import subprocess
import shutil

def setup_database():
    """Set up the database tables and seed initial data"""
    print("Setting up database...")
    
    # Initialize database
    try:
        subprocess.run([sys.executable, "scripts/init_db.py"], check=True)
        
        # Seed courses
        subprocess.run([sys.executable, "scripts/seed_courses.py"], check=True)
        
        # Seed challenges
        subprocess.run([sys.executable, "scripts/seed_challenges.py"], check=True)
        
        print("Database setup complete!")
    except subprocess.CalledProcessError as e:
        print(f"Error during database setup: {e}")
        print("Check the error message above and ensure SQL Server is running and accessible.")
        sys.exit(1)

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
            f.write("DATABASE_URL=mssql+pyodbc://localhost/Pythonchick?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes\n")
        
        print("Created .env file with default settings")
    else:
        print(".env file already exists")
    
    print("Environment setup complete!")

def create_venv():
    """Create and set up virtual environment"""
    print("Setting up virtual environment...")
    
    # Check if venv directory exists
    if os.path.exists("venv"):
        print("Virtual environment already exists. Skipping creation.")
    else:
        # Create virtual environment
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("Virtual environment created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            print("Continuing without creating a new virtual environment...")
    
    # Determine the pip path based on the OS
    if os.name == 'nt':  # Windows
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:  # Unix/Linux/Mac
        pip_path = os.path.join("venv", "bin", "pip")
    
    # Install dependencies using requirements.txt
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print("Please check your requirements.txt file and try again.")
        sys.exit(1)

def fix_model_conflicts():
    """Fix model conflicts by removing duplicate model definitions"""
    print("Fixing model conflicts...")
    
    # Backup the original file
    coding_challenge_path = "app/models/coding_challenge.py"
    backup_path = "app/models/coding_challenge.py.bak"
    
    if os.path.exists(coding_challenge_path):
        # Make a backup
        shutil.copy2(coding_challenge_path, backup_path)
        print(f"Created backup at {backup_path}")
        
        # Update the coding_challenge.py file to use extend_existing=True
        with open(coding_challenge_path, "r") as f:
            content = f.read()
        
        # Add extend_existing=True to the table definition
        updated_content = content.replace(
            "__tablename__ = \"coding_challenges\"",
            "__tablename__ = \"coding_challenges\"\n    __table_args__ = {'extend_existing': True}"
        )
        
        with open(coding_challenge_path, "w") as f:
            f.write(updated_content)
        
        print("Updated coding_challenge model to avoid conflicts")
    else:
        print(f"Warning: {coding_challenge_path} not found. Skipping fix.")

def main():
    """Main setup function"""
    print("Pythonchick Setup")
    print("=================")
    
    create_venv()
    setup_environment()
    fix_model_conflicts()
    setup_database()
    
    print("\nSetup completed successfully!")
    print("To start the API server, run: python run.py --reload")
    print("To start the frontend, run: cd ../frontend && npm start")

if __name__ == "__main__":
    main()