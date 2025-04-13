#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run database initialization
python scripts/init_db.py

# Apply database migrations
alembic upgrade head

# Seed courses
python scripts/seed_courses.py

# Seed challenges
python scripts/seed_challenges.py

# Seed games
python scripts/seed_games.py

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}