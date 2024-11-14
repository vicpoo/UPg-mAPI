from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.question import Question
from app.schemas.question_schema import QuestionCreate, QuestionResponse
from app.shared.config.db import get_db

questionRoutes = APIRouter()

@questionRoutes.post('/question/', response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    """Create a new question."""
    db_question = Question(**question.dict())
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question

@questionRoutes.get('/questions/', response_model=List[QuestionResponse])
async def get_questions(db: AsyncSession = Depends(get_db)):
    """Retrieve all questions."""
    result = await db.execute(select(Question))
    questions = result.scalars().all()
    return questions

@questionRoutes.get('/question/{question_id}', response_model=QuestionResponse)
async def get_question_by_id(question_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a question by ID."""
    result = await db.execute(select(Question).filter(Question.id == question_id))
    question = result.scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@questionRoutes.put('/question/{question_id}', response_model=QuestionResponse)
async def update_question(question_id: int, question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    """Update a question by ID."""
    result = await db.execute(select(Question).filter(Question.id == question_id))
    db_question = result.scalar_one_or_none()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    for key, value in question.dict().items():
        setattr(db_question, key, value)
    await db.commit()
    await db.refresh(db_question)
    return db_question

@questionRoutes.delete('/question/{question_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a question by ID."""
    result = await db.execute(select(Question).filter(Question.id == question_id))
    db_question = result.scalar_one_or_none()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    await db.delete(db_question)
    await db.commit()
    return {"message": "Question deleted"}
