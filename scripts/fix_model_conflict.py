# fix_model_conflict.py
import os
import shutil

def fix_model_conflicts():
    """Fix model conflicts by updating table definitions"""
    print("Fixing model conflicts...")
    
    # Paths to the model files
    coding_challenge_path = "app/models/coding_challenge.py"
    challenge_path = "app/models/challenge.py"
    
    # Backup and fix coding_challenge.py
    if os.path.exists(coding_challenge_path):
        # Create backup
        backup_path = f"{coding_challenge_path}.bak"
        shutil.copy2(coding_challenge_path, backup_path)
        print(f"Created backup at {backup_path}")
        
        # Update the table definition
        with open(coding_challenge_path, "r") as f:
            content = f.read()
        
        updated_content = content.replace(
            "__tablename__ = \"coding_challenges\"",
            "__tablename__ = \"coding_challenges\"\n    __table_args__ = {'extend_existing': True}"
        )
        
        with open(coding_challenge_path, "w") as f:
            f.write(updated_content)
        
        print(f"Updated {coding_challenge_path} to use extend_existing=True")
    
    # Backup and fix challenge.py
    if os.path.exists(challenge_path):
        # Create backup
        backup_path = f"{challenge_path}.bak"
        shutil.copy2(challenge_path, backup_path)
        print(f"Created backup at {backup_path}")
        
        # Update the table definition for CodingChallenge in challenge.py
        with open(challenge_path, "r") as f:
            content = f.read()
        
        updated_content = content.replace(
            "class CodingChallenge(Base):",
            "class CodingChallenge(Base):\n    __table_args__ = {'extend_existing': True}"
        )
        
        with open(challenge_path, "w") as f:
            f.write(updated_content)
        
        print(f"Updated {challenge_path} to use extend_existing=True")
    
    print("Model conflict fixes applied successfully!")

if __name__ == "__main__":
    fix_model_conflicts()
    print("You can now run 'python setup.py' to set up your backend")