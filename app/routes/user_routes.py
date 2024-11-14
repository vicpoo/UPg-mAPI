# user_routes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.shared.config.db import get_db

userRoutes = APIRouter()

@userRoutes.post('/user/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user."""
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()  # Cambiado a await db.commit()
    await db.refresh(db_user)  # Cambiado a await db.refresh(db_user)
    return db_user

@userRoutes.get('/users/', response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    """Retrieve all users."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@userRoutes.put('/user/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Update a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@userRoutes.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted"}
