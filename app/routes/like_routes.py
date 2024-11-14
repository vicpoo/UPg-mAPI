from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.like import Like
from app.schemas.like_schema import LikeCreate, LikeResponse
from app.shared.config.db import get_db

likeRoutes = APIRouter()

@likeRoutes.post('/like/', response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
async def create_like(like: LikeCreate, db: Session = Depends(get_db)):
    """Create a new like."""
    db_like = Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

@likeRoutes.get('/like/', response_model=List[LikeResponse])
async def get_likes(db: Session = Depends(get_db)):
    """Retrieve all likes."""
    likes = db.query(Like).all()
    return likes

@likeRoutes.delete('/like/{like_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(like_id: int, db: Session = Depends(get_db)):
    """Delete a like by ID."""
    db_like = db.query(Like).filter(Like.id == like_id).first()
    if db_like is None:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(db_like)
    db.commit()
    return {"message": "Like deleted"}

