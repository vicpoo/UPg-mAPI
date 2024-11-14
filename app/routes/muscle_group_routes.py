from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.muscle_group import MuscleGroup
from app.schemas.muscle_group_schema import MuscleGroupCreate, MuscleGroupResponse
from app.shared.config.db import get_db

muscleGroupRoutes = APIRouter()

# Crear un nuevo grupo muscular
@muscleGroupRoutes.post('/muscle-group/', response_model=MuscleGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_muscle_group(muscle_group: MuscleGroupCreate, db: AsyncSession = Depends(get_db)):
    db_muscle_group = MuscleGroup(**muscle_group.dict())
    db.add(db_muscle_group)
    await db.commit()
    await db.refresh(db_muscle_group)
    return db_muscle_group

# Obtener todos los grupos musculares
@muscleGroupRoutes.get('/muscle-group/', response_model=list[MuscleGroupResponse])
async def get_muscle_groups(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MuscleGroup))
    muscle_groups = result.scalars().all()
    return muscle_groups

# Obtener un grupo muscular por ID
@muscleGroupRoutes.get('/muscle-group/{muscle_group_id}', response_model=MuscleGroupResponse)
async def get_muscle_group(muscle_group_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MuscleGroup).filter(MuscleGroup.id == muscle_group_id))
    muscle_group = result.scalar_one_or_none()
    if muscle_group is None:
        raise HTTPException(status_code=404, detail="Grupo muscular no encontrado")
    return muscle_group

# Actualizar un grupo muscular
@muscleGroupRoutes.put('/muscle-group/{muscle_group_id}', response_model=MuscleGroupResponse)
async def update_muscle_group(muscle_group_id: int, muscle_group: MuscleGroupCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MuscleGroup).filter(MuscleGroup.id == muscle_group_id))
    db_muscle_group = result.scalar_one_or_none()
    if db_muscle_group is None:
        raise HTTPException(status_code=404, detail="Grupo muscular no encontrado")
    for key, value in muscle_group.dict().items():
        setattr(db_muscle_group, key, value)
    await db.commit()
    await db.refresh(db_muscle_group)
    return db_muscle_group

# Eliminar un grupo muscular
@muscleGroupRoutes.delete('/muscle-group/{muscle_group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_muscle_group(muscle_group_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MuscleGroup).filter(MuscleGroup.id == muscle_group_id))
    db_muscle_group = result.scalar_one_or_none()
    if db_muscle_group is None:
        raise HTTPException(status_code=404, detail="Grupo muscular no encontrado")
    await db.delete(db_muscle_group)
    await db.commit()
    return {"message": "Grupo muscular eliminado"}
