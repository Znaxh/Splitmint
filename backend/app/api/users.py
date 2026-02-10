"""
User API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.database import User
from app.schemas.schemas import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user (called after Clerk authentication).
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.clerk_user_id == user.clerk_user_id).first()
    if existing_user:
        return existing_user
    
    # Create new user
    db_user = User(
        clerk_user_id=user.clerk_user_id,
        email=user.email,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/{clerk_user_id}", response_model=UserResponse)
async def get_user_by_clerk_id(clerk_user_id: str, db: Session = Depends(get_db)):
    """
    Get user by Clerk user ID.
    """
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all users (for debugging/admin purposes).
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users
