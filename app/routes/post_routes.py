# post_routes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.post import Post
from app.schemas.post_schema import PostCreate, PostResponse
from app.shared.config.db import get_db

postRoutes = APIRouter()

@postRoutes.post('/post/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    """Create a new post."""
    db_post = Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@postRoutes.get('/posts/', response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    """Retrieve all posts."""
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts

@postRoutes.get('/post/{post_id}', response_model=PostResponse)
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a post by ID."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@postRoutes.put('/post/{post_id}', response_model=PostResponse)
async def update_post(post_id: int, post: PostCreate, db: AsyncSession = Depends(get_db)):
    """Update an existing post by ID."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@postRoutes.delete('/post/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a post by ID."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(db_post)
    await db.commit()
    return {"message": "Post deleted"}
