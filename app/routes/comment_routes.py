from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.shared.config.db import get_db
from typing import List 

commentRoutes = APIRouter()

# Crear un comentario
@commentRoutes.post('/comment/', response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Obtener todos los comentarios de una publicación
@commentRoutes.get('/comments/{post_id}', response_model=List[CommentResponse])
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.publicacion_id == post_id).all()
    return comments
