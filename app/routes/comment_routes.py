from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.comment import Comment
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.shared.config.db import get_db


commentRoutes = APIRouter()

@commentRoutes.post('/comment/', response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    """Create a new comment."""
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

from sqlalchemy.orm import joinedload
from app.models.comment import Comment
from app.models.user import User # Importamos el modelo User
from app.schemas.comment_schema import CommentResponse

@commentRoutes.get('/comments/{post_id}', response_model=List[CommentResponse])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all comments for a given post."""
    result = await db.execute(
        select(Comment)
        .filter(Comment.publicacion_id == post_id)
        .options(joinedload(Comment.usuario))  # Asegúrate de cargar el usuario relacionado
    )
    comments = result.scalars().all()

    # Agregar el nombre y la foto del usuario al comentario, convertimos la foto a Base64
    for comment in comments:
        comment.usuario_nombre = comment.usuario.nombre_usuario
        comment.usuario_foto = CommentResponse.encode_image(comment.usuario.foto_perfil)
    
    return comments


@commentRoutes.put('/comment/{comment_id}', response_model=CommentResponse)
async def update_comment(comment_id: int, comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    """Update a comment by ID."""
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalars().first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    for key, value in comment.dict().items():
        setattr(db_comment, key, value)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@commentRoutes.delete('/comment/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a comment by ID."""
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalars().first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    await db.delete(db_comment)
    await db.commit()
    return {"message": "Comment deleted"}
