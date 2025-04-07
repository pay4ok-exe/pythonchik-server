# scripts/seed_challenges.py
import sys
import os
import json

# Add parent directory to path to import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.repositories.challenge import ChallengeRepository
from app.utils.database import SessionLocal

def seed_challenges():
    db = SessionLocal()
    
    try:
        challenge_repo = ChallengeRepository(db)
        
        # Define some sample challenges
        challenges = [
            {
                "title": "Hello, World!",
                "description": "Write a program that prints 'Hello, World!' to the console.",
                "difficulty": "beginner",
                "starter_code": "# Write your code here\n",
                "solution_code": "print('Hello, World!')",
                "expected_output": "Hello, World!",
                "hints": [
                    "Use the print() function",
                    "Make sure to include quotes around the text",
                    "Watch out for typos"
                ],
                "points": 10
            },
            {
                "title": "Sum of Numbers",
                "description": "Write a program that adds two numbers (5 and 3) and prints the result.",
                "difficulty": "beginner",
                "starter_code": "# Write your code here\n# Add 5 and 3 and print the result\n",
                "solution_code": "a = 5\nb = 3\nprint(a + b)",
                "expected_output": "8",
                "hints": [
                    "Create variables to store the numbers",
                    "Use the + operator to add them",
                    "Use print() to display the result"
                ],
                "points": 15
            },
            {
                "title": "Even Numbers",
                "description": "Write a program that prints all even numbers from 2 to 10.",
                "difficulty": "beginner",
                "starter_code": "# Write your code here\n# Print even numbers from 2 to 10\n",
                "solution_code": "for i in range(2, 11, 2):\n    print(i)",
                "expected_output": "2\n4\n6\n8\n10",
                "hints": [
                    "Use a for loop with range()",
                    "The range() function can take 3 arguments: start, stop, step",
                    "Think about what step value would give you only even numbers"
                ],
                "points": 20
            },
            {
                "title": "String Concatenation",
                "description": "Create two string variables containing your first and last name, then concatenate them and print the result.",
                "difficulty": "beginner",
                "starter_code": "# Write your code here\n# Create first_name and last_name variables\n# Concatenate and print them\n",
                "solution_code": "first_name = \"John\"\nlast_name = \"Doe\"\nprint(first_name + \" \" + last_name)",
                "expected_output": "John Doe",
                "hints": [
                    "Create two string variables",
                    "Use the + operator to concatenate strings",
                    "Don't forget the space between first and last name"
                ],
                "points": 15
            },
            {
                "title": "Celsius to Fahrenheit",
                "description": "Write a program that converts 25 degrees Celsius to Fahrenheit and prints the result.",
                "difficulty": "intermediate",
                "starter_code": "# Write your code here\n# Formula: F = (C * 9/5) + 32\n# Convert 25°C to Fahrenheit\n",
                "solution_code": "celsius = 25\nfahrenheit = (celsius * 9/5) + 32\nprint(fahrenheit)",
                "expected_output": "77.0",
                "hints": [
                    "Create a variable for the Celsius temperature",
                    "Apply the conversion formula: F = (C * 9/5) + 32",
                    "Print the result"
                ],
                "points": 25
            },
            {
                "title": "List Average",
                "description": "Calculate and print the average of the numbers in the list: [10, 15, 20, 25, 30]",
                "difficulty": "intermediate",
                "starter_code": "# Write your code here\nnumbers = [10, 15, 20, 25, 30]\n# Calculate and print the average\n",
                "solution_code": "numbers = [10, 15, 20, 25, 30]\naverage = sum(numbers) / len(numbers)\nprint(average)",
                "expected_output": "20.0",
                "hints": [
                    "Use the sum() function to get the total",
                    "Use the len() function to get the count",
                    "Divide the sum by the count to get the average"
                ],
                "points": 30
            }
        ]
        
        # Create each challenge
        for challenge_data in challenges:
            # Check if challenge already exists (based on title)
            existing_challenges = challenge_repo.get_all_challenges()
            exists = any(c.title == challenge_data["title"] for c in existing_challenges)
            
            if exists:
                print(f"Challenge '{challenge_data['title']}' already exists. Skipping.")
                continue
            
            # Create new challenge
            challenge = challenge_repo.create_challenge(
                title=challenge_data["title"],
                description=challenge_data["description"],
                difficulty=challenge_data["difficulty"],
                starter_code=challenge_data["starter_code"],
                solution_code=challenge_data["solution_code"],
                expected_output=challenge_data["expected_output"],
                hints=challenge_data["hints"],
                points=challenge_data["points"]
            )
            
            print(f"Added challenge: {challenge.title}")
        
        print("Database seeded with challenges successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_challenges()