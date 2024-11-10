from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.like import Like
from app.schemas.like_schema import LikeCreate, LikeResponse
from app.shared.config.db import get_db

likeRoutes = APIRouter()

# Crear un nuevo "like"
@likeRoutes.post('/like/', response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
async def create_like(like: LikeCreate, db: Session = Depends(get_db)):
    db_like = Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

# Obtener todos los "likes"
@likeRoutes.get('/like/', response_model=list[LikeResponse])
async def get_likes(db: Session = Depends(get_db)):
    likes = db.query(Like).all()
    return likes
