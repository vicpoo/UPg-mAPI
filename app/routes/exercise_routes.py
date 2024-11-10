from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.exercise import Exercise
from app.schemas.exercise_schema import ExerciseCreate, ExerciseResponse
from app.shared.config.db import get_db

exerciseRoutes = APIRouter()

# Crear un nuevo ejercicio
@exerciseRoutes.post('/exercise/', response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

# Obtener todos los ejercicios
@exerciseRoutes.get('/exercise/', response_model=list[ExerciseResponse])
async def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(Exercise).all()
    return exercises

# Obtener un ejercicio por ID
@exerciseRoutes.get('/exercise/{exercise_id}', response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return exercise

# Actualizar un ejercicio
@exerciseRoutes.put('/exercise/{exercise_id}', response_model=ExerciseResponse)
async def update_exercise(exercise_id: int, exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    for key, value in exercise.dict().items():
        setattr(db_exercise, key, value)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

# Eliminar un ejercicio
@exerciseRoutes.delete('/exercise/{exercise_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    db.delete(db_exercise)
    db.commit()
    return {"message": "Ejercicio eliminado"}
