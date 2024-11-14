from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.exercise import Exercise
from app.schemas.exercise_schema import ExerciseCreate, ExerciseResponse
from app.shared.config.db import get_db

exerciseRoutes = APIRouter()

@exerciseRoutes.post('/exercise/', response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(exercise: ExerciseCreate, db: AsyncSession = Depends(get_db)):
    """Create a new exercise."""
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    await db.commit()
    await db.refresh(db_exercise)
    return db_exercise

@exerciseRoutes.get('/exercise/', response_model=List[ExerciseResponse])
async def get_exercises(db: AsyncSession = Depends(get_db)):
    """Retrieve all exercises."""
    result = await db.execute(select(Exercise))
    exercises = result.scalars().all()
    return exercises

@exerciseRoutes.get('/exercise/{exercise_id}', response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve an exercise by ID."""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@exerciseRoutes.put('/exercise/{exercise_id}', response_model=ExerciseResponse)
async def update_exercise(exercise_id: int, exercise: ExerciseCreate, db: AsyncSession = Depends(get_db)):
    """Update an existing exercise."""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    db_exercise = result.scalar_one_or_none()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    for key, value in exercise.dict().items():
        setattr(db_exercise, key, value)
    await db.commit()
    await db.refresh(db_exercise)
    return db_exercise

@exerciseRoutes.delete('/exercise/{exercise_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(exercise_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an exercise."""
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    db_exercise = result.scalar_one_or_none()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    await db.delete(db_exercise)
    await db.commit()
    return {"message": "Exercise deleted"}
