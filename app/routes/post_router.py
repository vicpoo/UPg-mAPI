from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.forum_posts import ForumPosts
from app.schemas.post_schema import PostCreate, PostResponse
from app.shared.config.db import get_db
from app.routes.userRouter import get_current_user

postRoutes = APIRouter()

# Crear un nuevo post
@postRoutes.post('/post/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_post = ForumPosts(
        **post.model_dump(exclude={'publication_date'}),
        publication_date=datetime.now(),
        user_id=current_user.id_user
    )
    db.add(db_post)
    db.commit()
    return db_post

@postRoutes.get('/post/', response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(ForumPosts).all()
    return posts

# Obtener un post por ID
@postRoutes.get('/post/{id_post}', response_model=PostResponse)
async def get_post_by_id(id_post: int, db: Session = Depends(get_db)):
    post = db.query(ForumPosts).filter(ForumPosts.id_post == id_post).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# Actualizar un post
@postRoutes.put('/post/{id_post}', response_model=PostResponse)
async def update_post(id_post: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(ForumPosts).filter(ForumPosts.id_post == id_post).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    return db_post

# Eliminar un post
@postRoutes.delete('/post/{id_post}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id_post: int, db: Session = Depends(get_db)):
    db_post = db.query(ForumPosts).filter(ForumPosts.id_post == id_post).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(db_post)
    db.commit()

# Obtener posts por ID de foro
@postRoutes.get('/posts/forum/{forum_id}', response_model=List[PostResponse])
async def get_posts_by_forum_id(forum_id: int, db: Session = Depends(get_db)):
    posts = db.query(ForumPosts).filter(ForumPosts.forum_id == forum_id).all()
    return posts

