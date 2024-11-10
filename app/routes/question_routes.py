from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question_schema import QuestionCreate, QuestionResponse
from app.shared.config.db import get_db
from typing import List 

questionRoutes = APIRouter()

# Crear una pregunta
@questionRoutes.post('/question/', response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Obtener todas las preguntas
@questionRoutes.get('/questions/', response_model=List[QuestionResponse])
async def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions
