from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.like import Like
from app.schemas.like_schema import LikeCreate, LikeResponse
from app.shared.config.db import get_db

likeRoutes = APIRouter()

@likeRoutes.post('/like/', response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
async def create_like(like: LikeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new like."""
    db_like = Like(**like.dict())
    db.add(db_like)
    await db.commit()
    await db.refresh(db_like)
    return db_like

@likeRoutes.get('/like/', response_model=List[LikeResponse])
async def get_likes(db: AsyncSession = Depends(get_db)):
    """Retrieve all likes."""
    result = await db.execute(select(Like))
    likes = result.scalars().all()
    return likes

@likeRoutes.delete('/like/{like_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(like_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a like by ID."""
    result = await db.execute(select(Like).filter(Like.id == like_id))
    db_like = result.scalar_one_or_none()
    if db_like is None:
        raise HTTPException(status_code=404, detail="Like not found")
    await db.delete(db_like)
    await db.commit()
    return {"message": "Like deleted"}
