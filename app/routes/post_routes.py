from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post_schema import PostCreate, PostResponse
from app.shared.config.db import get_db
from typing import List 

postRoutes = APIRouter()

# Crear una publicación
@postRoutes.post('/post/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Obtener todas las publicaciones
@postRoutes.get('/posts/', response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

# Obtener una publicación por ID
@postRoutes.get('/post/{post_id}', response_model=PostResponse)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return post
