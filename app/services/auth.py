# app/services/auth.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import TokenData
from app.utils.security import verify_password
from app.utils.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

class AuthService:
    def __init__(self, db: Session = None):
        self.db = db
        self.user_repository = UserRepository(db) if db else None
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        try:
            user = self.user_repository.get_by_username(username)
            if not user:
                return None
            if not verify_password(password, user.hashed_password):
                return None
            return user
        except Exception as e:
            print(f"Error in authenticate_user: {str(e)}")
            return None
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return encoded_jwt
        except Exception as e:
            print(f"Error in create_access_token: {str(e)}")
            raise e
    
    # Important: Make this a "callable" method to work properly with FastAPI dependency injection
    def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError as e:
            print(f"JWT Error: {str(e)}")
            raise credentials_exception
        except Exception as e:
            print(f"Unexpected error in get_current_user: {str(e)}")
            raise credentials_exception
        
        try:
            # Use the provided db session from dependency
            user_repository = UserRepository(db)
            user = user_repository.get_by_username(token_data.username)
            
            if user is None:
                raise credentials_exception
                
            return user
        except SQLAlchemyError as e:
            print(f"Database error in get_current_user: {str(e)}")
            raise credentials_exception
        except Exception as e:
            print(f"Error getting user in get_current_user: {str(e)}")
            raise credentials_exception