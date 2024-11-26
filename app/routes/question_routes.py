from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.question import Question
from app.models.user import User
from app.schemas.question_schema import QuestionCreate, QuestionResponse
from app.shared.config.db import get_db
from sqlalchemy.orm import selectinload  # Para cargar relaciones
import base64

questionRoutes = APIRouter()

def encode_image(image_data: bytes | str) -> str:
    """Convierte los datos de la imagen en formato base64."""
    if isinstance(image_data, str):
        return f"data:image/jpeg;base64,{image_data}"
    elif isinstance(image_data, bytes):
        return f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
    return None

@questionRoutes.post('/question/', response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    """
    Crear una nueva pregunta.
    Verifica que el usuario existe antes de asignarle la pregunta.
    """
    # Verificar si el usuario existe
    user_result = await db.execute(select(User).filter(User.id == question.usuario_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe"
        )
    
    # Crear la pregunta
    db_question = Question(**question.dict())
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    
    # Adjuntar datos del usuario para la respuesta
    if db_question.usuario and db_question.usuario.foto_perfil:
        db_question.usuario.foto_perfil = encode_image(db_question.usuario.foto_perfil)

    return db_question


@questionRoutes.get('/questions/', response_model=List[QuestionResponse])
async def get_all_questions(db: AsyncSession = Depends(get_db)):
    """Retrieve all questions, including user data."""
    result = await db.execute(
        select(Question)
        .options(joinedload(Question.usuario))  # Cargar relación con usuario
    )
    questions = result.scalars().all()

    # Procesar datos de usuario
    for question in questions:
      if question.usuario and question.usuario.foto_perfil:
         question.usuario.foto_perfil = encode_image(question.usuario.foto_perfil)



    return questions





@questionRoutes.get('/question/{question_id}', response_model=QuestionResponse)
async def get_question_by_id(question_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a question by ID, including user data."""
    result = await db.execute(
        select(Question)
        .options(joinedload(Question.usuario))
        .filter(Question.id == question_id)
    )
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.usuario and question.usuario.foto_perfil:
        question.usuario.foto_perfil = encode_image(question.usuario.foto_perfil)

    return question


@questionRoutes.put('/question/{question_id}', response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question: QuestionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update a question by ID."""
    result = await db.execute(select(Question).filter(Question.id == question_id))
    db_question = result.scalar_one_or_none()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question.dict().items():
        setattr(db_question, key, value)

    await db.commit()
    await db.refresh(db_question)

    if db_question.usuario and db_question.usuario.foto_perfil:
        db_question.usuario.foto_perfil = encode_image(db_question.usuario.foto_perfil)

    return db_question


@questionRoutes.delete('/question/{question_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a question by ID."""
    result = await db.execute(select(Question).filter(Question.id == question_id))
    db_question = result.scalar_one_or_none()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    await db.delete(db_question)
    await db.commit()
    return {"message": "Question deleted"}


@questionRoutes.get('/admin/questions/', response_model=List[QuestionResponse])
async def get_all_questions_no_middleware(db: AsyncSession = Depends(get_db)):
    """
    Recuperar todas las preguntas sin usar middleware.
    Diseñado para vistas administrativas.
    """
    result = await db.execute(
        select(Question)
        .options(joinedload(Question.usuario))  # Cargar relación con usuario
    )
    questions = result.scalars().all()

    # Procesar datos de usuario
    for question in questions:
        if question.usuario and question.usuario.foto_perfil:
            question.usuario.foto_perfil = encode_image(question.usuario.foto_perfil)

    return questions


@questionRoutes.delete('/admin/question/{question_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_question_no_middleware(question_id: int, db: AsyncSession = Depends(get_db)):
    """
    Eliminar una pregunta por ID sin usar middleware.
    Diseñado para vistas administrativas.
    """
    result = await db.execute(select(Question).filter(Question.id == question_id))
    db_question = result.scalar_one_or_none()

    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Esto eliminará la pregunta y sus respuestas asociadas en cascada
    await db.delete(db_question)
    await db.commit()

    return {"message": "Question deleted"}
