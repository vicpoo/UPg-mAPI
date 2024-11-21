from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.like import Like
from app.schemas.like_schema import LikeCreate, LikeResponse
from app.shared.config.db import get_db

likeRoutes = APIRouter()

@likeRoutes.post('/like/', response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
async def create_like(like: LikeCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new like.
    - **publicacion_id**: ID de la publicación a la que se da like.
    - **usuario_id**: ID del usuario que da like.
    """
    # Verificar si el like ya existe
    result = await db.execute(
        select(Like).filter(Like.publicacion_id == like.publicacion_id, Like.usuario_id == like.usuario_id)
    )
    existing_like = result.scalar_one_or_none()
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya dio like a esta publicación"
        )
    # Crear el nuevo like
    db_like = Like(**like.dict())
    db.add(db_like)
    await db.commit()
    await db.refresh(db_like)
    return db_like

@likeRoutes.get('/like/', response_model=List[LikeResponse])
async def get_likes(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Retrieve paginated likes.
    - **skip**: Número de registros a saltar (default: 0).
    - **limit**: Número máximo de registros a devolver (default: 10).
    """
    result = await db.execute(select(Like).offset(skip).limit(limit))
    likes = result.scalars().all()
    return likes

@likeRoutes.delete('/like/{like_id}', response_model=dict, status_code=status.HTTP_200_OK)
async def delete_like(like_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a like by ID.
    - **like_id**: ID del like a eliminar.
    """
    result = await db.execute(select(Like).filter(Like.id == like_id))
    db_like = result.scalar_one_or_none()
    if db_like is None:
        raise HTTPException(status_code=404, detail="Like not found")
    await db.delete(db_like)
    await db.commit()
    return {"message": f"Like con ID {like_id} eliminado correctamente"}

@likeRoutes.get('/like/count/', response_model=int, status_code=status.HTTP_200_OK)
async def count_likes(publicacion_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    """
    Count the total likes or likes for a specific publication.
    - **publicacion_id**: (opcional) ID de la publicación para contar likes.
    """
    query = select(Like)
    if publicacion_id:
        query = query.filter(Like.publicacion_id == publicacion_id)
    result = await db.execute(query)
    count = len(result.scalars().all())
    return count
