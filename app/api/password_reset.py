# app/api/password_reset.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets
import string
from app.utils.database import get_db
from app.repositories.user import UserRepository
from app.utils.email import EmailService
from app.utils.security import get_password_hash

router = APIRouter(prefix="/auth", tags=["authentication"])

class PasswordResetRequest(BaseModel):
    email: EmailStr

class VerifyResetTokenRequest(BaseModel):
    email: EmailStr
    token: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str

# Store reset tokens temporarily (in a real app, you'd use Redis or a database table)
# Format: {email: {'token': 'abc123', 'expires': datetime_obj}}
reset_tokens = {}

def generate_reset_token(length=32):
    """Generate a secure random token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@router.post("/forgot-password")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    # Find the user by email
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(request.email)
    
    if not user:
        # Don't reveal whether the user exists for security reasons
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # Generate a reset token
    token = generate_reset_token()
    
    # Set token expiration (30 minutes)
    expiration = datetime.utcnow() + timedelta(minutes=30)
    
    # Store token
    reset_tokens[request.email] = {
        'token': token,
        'expires': expiration
    }
    
    # Send reset email
    email_service = EmailService()
    email_sent = email_service.send_password_reset(
        to_email=request.email,
        reset_token=token,
        username=user.username
    )
    
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email"
        )
    
    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/verify-reset-token")
async def verify_reset_token(request: VerifyResetTokenRequest):
    # Check if token exists and is valid
    token_data = reset_tokens.get(request.email)
    
    if not token_data or token_data['token'] != request.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    # Check if token is expired
    if token_data['expires'] < datetime.utcnow():
        # Remove expired token
        reset_tokens.pop(request.email, None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired"
        )
    
    return {"valid": True}

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    # Check if token exists and is valid
    token_data = reset_tokens.get(request.email)
    
    if not token_data or token_data['token'] != request.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    # Check if token is expired
    if token_data['expires'] < datetime.utcnow():
        # Remove expired token
        reset_tokens.pop(request.email, None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired"
        )
    
    # Get the user
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(request.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    hashed_password = get_password_hash(request.new_password)
    user.hashed_password = hashed_password
    db.commit()
    
    # Remove the token
    reset_tokens.pop(request.email, None)
    
    return {"message": "Password has been reset successfully"}